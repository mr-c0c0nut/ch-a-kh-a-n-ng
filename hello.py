
# COCO AI | Minimal Monitor

import sys
import subprocess

try:
    import requests
except ImportError:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "requests"
    ])
    import requests

# API CONFIG
API_KEYS = [
    "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",
    "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"
]

MODEL = "openai/gpt-4o-mini"
URL = "https://openrouter.ai/api/v1/chat/completions"

# MEMORY
messages = [{
    "role": "system",
    "content": (
        "You are COCO AI. Be concise and helpful. "
        "When providing code, use Markdown code blocks "
        "with the correct language identifier."
    )
}]

def ask(prompt):
    messages.append({"role": "user", "content": prompt})

    for key in API_KEYS:
        if not key or key.startswith("YOUR_"):
            continue

        try:
            r = requests.post(
                URL,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL,
                    "messages": messages
                },
                timeout=45
            )

            r.raise_for_status()
            answer = r.json()["choices"][0]["message"]["content"]

            messages.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        except requests.RequestException:
            continue

        except (KeyError, IndexError, ValueError):
            continue

    messages.pop()
    return "Connection unavailable. Please try again."

# MAIN
print("COCO AI | Monitor Online")

while True:
    try:
        prompt = input("\nYou > ").strip()

        if prompt.lower() in ("exit", "quit"):
            break

        if prompt:
            print("\n" + ask(prompt))

    except KeyboardInterrupt:
        print("\nCOCO AI | Offline")
        break
