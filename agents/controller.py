from agents.student_query_agent import StudentQueryAgent
from agents.bkt_agent import BKTEngine
from agents.rl_quiz_agent import AdaptiveQuizAgent


class MultiAgentController:
    """
    Central controller that orchestrates interactions between:
    - Student Query Agent (LLM)
    - Assessment Agent (BKT)
    - Adaptive Quiz Agent (RL)
    """

    def __init__(self):
        self.query_agent = StudentQueryAgent()
        self.bkt_agent = BKTEngine()
        self.rl_agent = AdaptiveQuizAgent()

    def handle_student_query(self, student_id: str, question: str) -> dict:
        """
        Process a student's natural language query using the LLM agent.
        """
        response = self.query_agent.answer_question(
            student_id=student_id,
            question=question
        )

        return {
            "student_id": student_id,
            "question": question,
            "answer": response
        }

    def assess_response(self, student_id: str, skill_id: str, is_correct: bool) -> dict:
        """
        Update student mastery using BKT after an attempt.
        """
        mastery = self.bkt_agent.update_skill(
            student_id=student_id,
            skill_id=skill_id,
            is_correct=is_correct
        )

        return {
            "student_id": student_id,
            "skill_id": skill_id,
            "mastery": mastery
        }

    def get_next_quiz(self, student_id: str, skill_id: str) -> dict:
        """
        Decide the next quiz action using the RL agent.
        """
        mastery = self.bkt_agent.get_mastery(
            student_id=student_id,
            skill_id=skill_id
        )
	
        decision = self.rl_agent.select_action(
            student_id=student_id,
            mastery=mastery
        )

        return {
            "student_id": student_id,
            "skill_id": skill_id,
            "mastery": mastery,
            "state": decision["state"],
            "action": decision["action"]
        }
    def decide_difficulty_from_analytics(self, summary: dict) -> str:
        """
        Decide quiz difficulty based on learning analytics.
        """
        status = summary.get("trend") or summary.get("status")

        if status == "improving":
            return "HARD"
        elif status == "declining":
            return "EASY"
        else:
            return "MEDIUM"

