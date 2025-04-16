# filename: app.py
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # or hardcode your key here for testing

@app.route("/")
def home():
    return "AI Webhook is live!"

@app.route('/generate-ai', methods=['GET'])
def generate():
    company = request.args.get("company", "a company")
    role = request.args.get("role", "a role")
    value = request.args.get("value", "innovation")

    prompt = f"Write a 2-sentence paragraph about why someone is excited to apply for the {role} role at {company}, focusing on their value of {value}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes professional, enthusiastic job application content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    text = response['choices'][0]['message']['content'].strip()
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
