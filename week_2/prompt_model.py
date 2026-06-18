import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

AVAILABLE_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash",
}


def prompt_model(model: str, prompt: str) -> str:
    if model not in AVAILABLE_MODELS:
        return f"[Model Error] Unsupported model: {model}"

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        if not response.text:
            return "[Gemini Error] Empty response"

        return response.text

    except Exception as error:
        return f"[Gemini Error] {error}"


if __name__ == "__main__":
    result = prompt_model(
        "gemini-2.5-flash",
        "Tell me one short Malaysian joke",
    )

    print("--- RESPONSE ---")
    print(result)