from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Set this in Render

@app.route('/generate-ai', methods=['GET'])
def generate():
    company = request.args.get("company", "a company") or "a company"
    role = request.args.get("role", "a role") or "a role"
    value = request.args.get("value", "innovation") or "innovation"

    prompt = f"Write a 2-sentence paragraph about why someone is excited to apply for the {role} role at {company}, focusing on their value of {value}."

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",  # Required for OpenRouter usage
            "X-Title": "TextBlaze AI Integration"
        }

        body = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that writes professional, enthusiastic job application paragraphs."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        result = response.json()

        text = result['choices'][0]['message']['content'].strip()
        return jsonify({"text": text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"text": f"An error occurred: {e}"}), 500
