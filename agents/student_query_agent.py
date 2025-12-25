import requests


class StudentQueryAgent:
    """
    Handles student questions and returns responses using a local Ollama LLM.
    """

    def __init__(self, model_name: str = "qwen2.5:1.5b"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"

    def answer_question(self, student_id: str, question: str) -> dict:
        """
        Accepts a student question and returns a response.
        """

        payload = {
            "model": self.model_name,
            "prompt": question,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            answer = response.json().get("response", "").strip()

        except Exception as e:
            answer = f"Ollama error: {str(e)}"

        return {
            "student_id": student_id,
            "question": question,
            "answer": answer
        }
