import requests
import os

class StudentQueryAgent:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def answer_question(self, student_id: str, question: str) -> dict:
        if not self.api_key:
            return {
                "student_id": student_id,
                "question": question,
                "answer": "LLM API key not configured."
            }

        payload = {
            "inputs": f"Answer clearly with examples:\n{question}"
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return {
                "student_id": student_id,
                "question": question,
                "answer": "LLM service temporarily unavailable."
            }

        result = response.json()

        generated_text = result[0]["generated_text"] if isinstance(result, list) else str(result)

        return {
            "student_id": student_id,
            "question": question,
            "answer": generated_text
        }
