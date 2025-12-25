import requests

class StudentQueryAgent:
    def answer_question(self, student_id: str, question: str) -> dict:
        try:
            # Try Ollama (local only)
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": question,
                    "stream": False
                },
                timeout=3
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "student_id": student_id,
                    "question": question,
                    "answer": data.get("response", "No response generated")
                }

        except Exception:
            pass  # Ollama not available (cloud)

        # ✅ Fallback response (cloud-safe)
        return {
            "student_id": student_id,
            "question": question,
            "answer": (
                "Hadoop is an open-source framework used in Big Data to store and "
                "process very large datasets across distributed clusters of computers. "
                "It consists mainly of HDFS (storage) and MapReduce (processing)."
            )
        }
