from datetime import datetime


def bkt_state_document(student_id: str, skill_id: str, mastery: float) -> dict:
    """
    Create a BKT state document for persistence.
    """
    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "mastery": mastery,
        "updated_at": datetime.utcnow()
    }


def attempt_document(student_id: str, skill_id: str, is_correct: bool) -> dict:
    """
    Create an attempt log document.
    """
    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "is_correct": is_correct,
        "timestamp": datetime.utcnow()
    }

from datetime import datetime

def learning_history_document(
    student_id: str,
    skill_id: str,
    question: str,
    answer: str,
    is_correct: bool | None,
    mastery: float | None,
    quiz_action: str | None
):
    return {
        "student_id": student_id,
        "skill_id": skill_id,
        "question": question,
        "answer": answer,
        "is_correct": is_correct,
        "mastery": mastery,
        "quiz_action": quiz_action,
        "timestamp": datetime.utcnow()
    }
