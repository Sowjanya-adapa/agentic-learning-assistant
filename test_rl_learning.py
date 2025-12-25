from agents.rl_quiz_agent import AdaptiveQuizAgent

agent = AdaptiveQuizAgent()
student_id = "student_001"

# Initial mastery
mastery_before = 0.25
mastery_after = 0.40  # Simulate learning improvement

print("Initial Q-table:")
print(agent.q_table)

# Agent selects an action
decision = agent.select_action(student_id, mastery_before)
action = decision["action"]

# Compute reward
reward = agent.compute_reward(mastery_before, mastery_after)

# Update policy
agent.update_policy(
    student_id=student_id,
    mastery_before=mastery_before,
    mastery_after=mastery_after,
    reward=reward
)

print("\nAction taken:", action)
print("Reward received:", reward)

print("\nUpdated Q-table:")
print(agent.q_table)
