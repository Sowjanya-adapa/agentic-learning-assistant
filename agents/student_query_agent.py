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
    question_lower = question.lower()

    # ---------- Intelligent Rule-Based Fallback ----------
    if not self.api_key:
        if "java" in question_lower:
            answer = (
                "Java is a high-level, object-oriented programming language "
                "used to build platform-independent applications.\n\n"
                "Example:\n"
                "A banking system built in Java can run on Windows, Linux, or macOS "
                "using the Java Virtual Machine (JVM)."
            )
        elif "hadoop" in question_lower:
            answer = (
                "Hadoop is an open-source Big Data framework used for storing and "
                "processing large datasets across distributed systems.\n\n"
                "Example:\n"
                "Companies like Facebook use Hadoop to process petabytes of user data."
            )
        else:
            answer = (
                "This is a conceptual question. Please provide more context "
                "or specify the topic for a clearer explanation."
            )

        return {
            "student_id": student_id,
            "question": question,
            "answer": answer
        }

    # ---------- LLM-Based Answer (Primary Path) ----------
    payload = {
        "inputs": f"Answer clearly with explanation and examples:\n{question}"
    }

    try:
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception("LLM unavailable")

        result = response.json()
        generated_text = result[0]["generated_text"]

        return {
            "student_id": student_id,
            "question": question,
            "answer": generated_text
        }

    except Exception:
        return {
            "student_id": student_id,
            "question": question,
            "answer": "AI service is temporarily unavailable. Please try again later."
        }
