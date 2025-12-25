class AdaptiveQuizAgent:
    """
    Reinforcement Learning agent for adaptive quiz selection.

    Uses:
    - Discrete state space (LOW, MEDIUM, HIGH)
    - Discrete action space (EASY, MEDIUM, HARD)
    - Tabular Q-learning
    """

    def __init__(self):
        # State and action spaces
        self.states = ["LOW", "MEDIUM", "HIGH"]
        self.actions = ["EASY", "MEDIUM", "HARD"]

        # Q-learning parameters
        self.alpha = 0.3   # learning rate
        self.gamma = 0.9   # discount factor
        self.epsilon = 0.1 # exploration rate

        # Initialize Q-table
        # Q[state][action] = value
        self.q_table = {
            state: {action: 0.0 for action in self.actions}
            for state in self.states
        }

    def _discretize_mastery(self, mastery: float) -> str:
        if mastery < 0.3:
            return "LOW"
        elif mastery < 0.7:
            return "MEDIUM"
        else:
            return "HIGH"

    def compute_reward(self, mastery_before: float, mastery_after: float) -> float:
        return mastery_after - mastery_before

    def select_action(self, student_id: str, mastery: float) -> dict:
        """
        ε-greedy action selection.
        """
        import random

        state = self._discretize_mastery(mastery)

        # Exploration
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            # Exploitation
            action = max(
                self.q_table[state],
                key=self.q_table[state].get
            )

        return {
            "student_id": student_id,
            "state": state,
            "action": action
        }

    def update_policy(
        self,
        student_id: str,
        mastery_before: float,
        mastery_after: float,
        reward: float
    ):
        """
        Update Q-table using Q-learning rule.
        """
        state = self._discretize_mastery(mastery_before)
        next_state = self._discretize_mastery(mastery_after)

        # Choose action that was taken (best guess: max-Q action)
        action = max(self.q_table[state], key=self.q_table[state].get)

        best_next_q = max(self.q_table[next_state].values())

        # Q-learning update
        old_q = self.q_table[state][action]
        new_q = old_q + self.alpha * (
            reward + self.gamma * best_next_q - old_q
        )

        self.q_table[state][action] = new_q
