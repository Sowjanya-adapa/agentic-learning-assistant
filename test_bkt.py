from agents.bkt_agent import BKTEngine

# Create BKT engine
bkt = BKTEngine()

student_id = "student_001"
skill_id = "linear_equations"

# Initialize skill
print("Initialize skill:")
print(bkt.initialize_skill(student_id, skill_id))

# Simulate attempts
attempts = [True, True, False, True]

print("\nSimulating attempts:")
for i, result in enumerate(attempts, start=1):
    update = bkt.update_skill(student_id, skill_id, result)
    print(f"Attempt {i} | Correct: {result} | Mastery: {update['mastery']}")
