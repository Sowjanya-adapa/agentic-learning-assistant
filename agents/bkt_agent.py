class BKTEngine:
    """
    Bayesian Knowledge Tracing (BKT) engine for tracking
    student mastery of individual skills.
    """

    def __init__(self):
        # BKT parameters
        self.p_init = 0.2
        self.p_learn = 0.1
        self.p_guess = 0.2
        self.p_slip = 0.1

        # In-memory knowledge state
        self.knowledge_state = {}

    def initialize_skill(self, student_id: str, skill_id: str) -> dict:
        """
        Initialize BKT state for a student-skill pair.
        """
        self.knowledge_state[(student_id, skill_id)] = self.p_init
        return {
            "student_id": student_id,
            "skill_id": skill_id,
            "mastery": self.p_init
        }

    def update_skill(self, student_id: str, skill_id: str, is_correct: bool) -> dict:
        """
        Update mastery probability using BKT equations.
        """
        key = (student_id, skill_id)

        if key not in self.knowledge_state:
            self.initialize_skill(student_id, skill_id)

        p_know = self.knowledge_state[key]

        if is_correct:
            numerator = p_know * (1 - self.p_slip)
            denominator = numerator + (1 - p_know) * self.p_guess
            p_obs = numerator / denominator
        else:
            numerator = p_know * self.p_slip
            denominator = numerator + (1 - p_know) * (1 - self.p_guess)
            p_obs = numerator / denominator

        p_updated = p_obs + (1 - p_obs) * self.p_learn
        self.knowledge_state[key] = p_updated

        return {
            "student_id": student_id,
            "skill_id": skill_id,
            "is_correct": is_correct,
            "mastery": round(p_updated, 4)
        }

    def get_mastery(self, student_id: str, skill_id: str) -> float:
        """
        Get current mastery probability.
        """
        return self.knowledge_state.get((student_id, skill_id), 0.0)
