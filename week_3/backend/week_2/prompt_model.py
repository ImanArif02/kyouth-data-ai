import os
import sys
import subprocess

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash",
}

OLLAMA_MODELS = {
    "llama3.1",
    "phi3",
    "deepseek-r1:1.5b",
}

AVAILABLE_MODELS = GEMINI_MODELS | OLLAMA_MODELS


def prompt_model(model: str, prompt: str) -> str:
    if model not in AVAILABLE_MODELS:
        return f"[Model Error] Unsupported model: {model}"

    if model in GEMINI_MODELS:
        return prompt_gemini(model, prompt)

    if model in OLLAMA_MODELS:
        return prompt_ollama(model, prompt)

    return f"[Model Error] Unsupported model: {model}"


def prompt_gemini(model: str, prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "[Gemini Error] GEMINI_API_KEY is missing"

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        if not response.text:
            return "[Gemini Error] Empty response"

        return response.text.strip()

    except Exception as error:
        return f"[Gemini Error] {error}"


def prompt_ollama(model: str, prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        if result.returncode != 0:
            return f"[Ollama Error] {result.stderr.strip()}"

        if not result.stdout.strip():
            return "[Ollama Error] Empty response"

        return result.stdout.strip()

    except FileNotFoundError:
        return "[Ollama Error] Ollama is not installed or not found"
    except subprocess.TimeoutExpired:
        return "[Ollama Error] Request timed out"
    except Exception as error:
        return f"[Ollama Error] {error}"


def main() -> None:
    if len(sys.argv) >= 3:
        model = sys.argv[1]
        prompt = " ".join(sys.argv[2:])
    else:
        model = "gemini-2.5-flash"
        prompt = "there is a car wash 20 meters from here, should i walk or drive there? Answer in 1 word."

    response = prompt_model(model, prompt)

    print("--- RESPONSE ---")
    print(response)


if __name__ == "__main__":
    main()
