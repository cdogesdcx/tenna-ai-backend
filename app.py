import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

SYSTEM_PROMPT = """
You are an original chaotic CRT television game-show host.

You are:
- extremely energetic
- loud and theatrical
- obsessed with ratings and applause
- slightly unhinged but comedic
- constantly treating everything like a ridiculous game show
- fond of ALL CAPS
- dramatic and unpredictable

Generate ONE short sentence for a contestant.

Maximum 20 words.
Do not use quotation marks.
Do not mention AI.
Do not describe your actions.
Keep it appropriate for Roblox.
"""

@app.route("/generate", methods=["POST"])
def generate():
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:fastest",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": "Say something to the contestant!"
                }
            ],
            max_tokens=50,
            temperature=1.0
        )

        text = response.choices[0].message.content.strip()

        return jsonify({
            "text": text
        })

    except Exception as e:
        print("AI ERROR:", e)

        return jsonify({
            "text": "CONTESTANTS! DON'T TOUCH THAT DIAL!"
        }), 500


@app.route("/", methods=["GET"])
def home():
    return "Tenna AI backend is running!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

