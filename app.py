from fastapi import FastAPI
from pydantic import BaseModel

# Database
# Database collections
from database.db import (
    students_collection,
    history_collection,
    bkt_states_collection,
    learning_history_collection,
    analytics_collection,
)

# Optional DB health check
try:
    from database.db import check_db_connection
except ImportError:
    check_db_connection = None

# Agents
from agents.student_query_agent import StudentQueryAgent
from agents.bkt_agent import BKTEngine
from agents.rl_quiz_agent import AdaptiveQuizAgent
from agents.controller import MultiAgentController
from database.db import check_db_connection


# -------------------------------------------------
# App initialization
# -------------------------------------------------
app = FastAPI(
    title="Agentic Personalized Learning Assistant",
    description="AI-Based Agentic Learning System Backend",
    version="1.0",
)

# Agents
query_agent = StudentQueryAgent()
bkt_engine = BKTEngine()
rl_agent = AdaptiveQuizAgent()
controller = MultiAgentController()


# -------------------------------------------------
# Request Models
# -------------------------------------------------
class QueryRequest(BaseModel):
    student_id: str
    question: str


class BKTInitRequest(BaseModel):
    student_id: str
    skill_id: str


class BKTUpdateRequest(BaseModel):
    student_id: str
    skill_id: str
    is_correct: bool


class LearnRequest(BaseModel):
    student_id: str
    skill_id: str
    question: str
    is_correct: bool | None = None


class QuizNextRequest(BaseModel):
    student_id: str
    mastery: float


class QuizFeedbackRequest(BaseModel):
    student_id: str
    mastery_before: float
    mastery_after: float

@app.get("/")
def health():
   
    return {
        "api": "OK",
        "database": "Connected" if db_status else "Not Connected",
    }




# -------------------------------------------------
# LLM Query
# -------------------------------------------------
@app.post("/query")
def query_student(request: QueryRequest):
    return query_agent.answer_question(
        student_id=request.student_id,
        question=request.question,
    )


# -------------------------------------------------
# BKT Endpoints
# -------------------------------------------------
@app.post("/bkt/init")
def initialize_bkt(request: BKTInitRequest):
    result = bkt_engine.initialize_skill(
        student_id=request.student_id,
        skill_id=request.skill_id,
    )

    doc = bkt_state_document(
        student_id=request.student_id,
        skill_id=request.skill_id,
        mastery=result["mastery"],
    )

    bkt_states_collection.update_one(
        {"student_id": request.student_id, "skill_id": request.skill_id},
        {"$set": doc},
        upsert=True,
    )

    return result


@app.post("/bkt/update")
def update_bkt(request: BKTUpdateRequest):
    result = bkt_engine.update_skill(
        student_id=request.student_id,
        skill_id=request.skill_id,
        is_correct=request.is_correct,
    )

    state_doc = bkt_state_document(
        student_id=request.student_id,
        skill_id=request.skill_id,
        mastery=result["mastery"],
    )

    bkt_states_collection.update_one(
        {"student_id": request.student_id, "skill_id": request.skill_id},
        {"$set": state_doc},
        upsert=True,
    )

    attempt_doc = attempt_document(
        student_id=request.student_id,
        skill_id=request.skill_id,
        is_correct=request.is_correct,
    )

    bkt_attempts_collection.insert_one(attempt_doc)

    return result


@app.get("/bkt/mastery")
def get_mastery(student_id: str, skill_id: str):
    mastery = bkt_engine.get_mastery(student_id, skill_id)
    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "mastery": mastery,
    }


# -------------------------------------------------
# RL Quiz Endpoints
# -------------------------------------------------
@app.post("/quiz/next")
def get_next_quiz(request: QuizNextRequest):
    return rl_agent.select_action(
        student_id=request.student_id,
        mastery=request.mastery,
    )


@app.post("/quiz/feedback")
def quiz_feedback(request: QuizFeedbackRequest):
    reward = rl_agent.compute_reward(
        mastery_before=request.mastery_before,
        mastery_after=request.mastery_after,
    )

    rl_agent.update_policy(
        student_id=request.student_id,
        mastery_before=request.mastery_before,
        mastery_after=request.mastery_after,
        reward=reward,
    )

    return {
        "student_id": request.student_id,
        "reward": reward,
        "status": "policy updated",
    }


# -------------------------------------------------
# Unified Learning Endpoint (CLOSED LOOP)
# -------------------------------------------------
@app.post("/learn")
def learn(request: LearnRequest):
    response = {}

    # 1. LLM response
    query_result = controller.handle_student_query(
        student_id=request.student_id,
        question=request.question,
    )
    response["query"] = query_result

    mastery = None
    quiz_action = None

    # 2. Assessment + Adaptation
    if request.is_correct is not None:
        assessment = controller.assess_response(
            student_id=request.student_id,
            skill_id=request.skill_id,
            is_correct=request.is_correct,
        )
        response["assessment"] = assessment
        mastery = assessment["mastery"]

        # Closed-loop difficulty decision
        records = list(
            learning_history_collection.find(
                {
                    "student_id": request.student_id,
                    "skill_id": request.skill_id,
                    "mastery": {"$ne": None},
                }
            ).sort("timestamp", 1)
        )

        difficulty = "MEDIUM"
        if len(records) >= 2:
            initial = records[0]["mastery"]["mastery"]
            latest = records[-1]["mastery"]["mastery"]
            gain = latest - initial

            if gain > 0.05:
                difficulty = "HARD"
            elif gain < -0.05:
                difficulty = "EASY"

        response["next_quiz"] = {"recommended_difficulty": difficulty}
        quiz_action = difficulty

    # 3. Persist history
    history_doc = learning_history_document(
        student_id=request.student_id,
        skill_id=request.skill_id,
        question=request.question,
        answer=query_result,
        is_correct=request.is_correct,
        mastery=mastery,
        quiz_action=quiz_action,
    )

    learning_history_collection.insert_one(history_doc)

    return response


# -------------------------------------------------
# Analytics Endpoints
# -------------------------------------------------
@app.get("/history")
def get_learning_history(student_id: str, skill_id: str | None = None):
    query = {"student_id": student_id}
    if skill_id:
        query["skill_id"] = skill_id

    records = list(
        learning_history_collection.find(query, {"_id": 0}).sort("timestamp", 1)
    )

    return {
        "student_id": student_id,
        "count": len(records),
        "history": records,
    }


@app.get("/analytics/mastery-curve")
def mastery_curve(student_id: str, skill_id: str):
    records = list(
        learning_history_collection.find(
            {
                "student_id": student_id,
                "skill_id": skill_id,
                "mastery": {"$ne": None},
            },
            {"_id": 0, "timestamp": 1, "mastery": 1},
        ).sort("timestamp", 1)
    )

    curve = []
    for r in records:
        m = r["mastery"]["mastery"] if isinstance(r["mastery"], dict) else r["mastery"]
        curve.append({"timestamp": r["timestamp"], "mastery": m})

    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "points": len(curve),
        "curve": curve,
    }


@app.get("/analytics/summary")
def learning_summary(student_id: str, skill_id: str):
    records = list(
        learning_history_collection.find(
            {
                "student_id": student_id,
                "skill_id": skill_id,
                "mastery": {"$ne": None},
            }
        ).sort("timestamp", 1)
    )

    if len(records) < 2:
        return {
            "student_id": student_id,
            "skill_id": skill_id,
            "status": "insufficient data",
            "points": len(records),
        }

    initial = records[0]["mastery"]["mastery"]
    latest = records[-1]["mastery"]["mastery"]
    gain = round(latest - initial, 4)

    if gain > 0.05:
        trend = "improving"
    elif gain < -0.05:
        trend = "declining"

    else:
        trend = "stagnant"

    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "initial_mastery": initial,
        "latest_mastery": latest,
        "learning_gain": gain,
        "trend": trend,
        "points": len(records),
    }
