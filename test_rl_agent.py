from agents.rl_quiz_agent import AdaptiveQuizAgent

# Create the RL agent
agent = AdaptiveQuizAgent()

student_id = "student_001"

# Test different mastery levels
test_mastery_values = [0.1, 0.5, 0.85]

print("Testing Adaptive Quiz Agent:\n")

for mastery in test_mastery_values:
    decision = agent.select_action(student_id, mastery)
    print(
        f"Mastery: {mastery:.2f} | "
        f"State: {decision['state']} | "
        f"Selected Action: {decision['action']}"
    )
