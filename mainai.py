from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

groq = Groq(api_key=api_key)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/ask", methods=['POST'])
def ask():

    question = request.form.get('question')

    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Act like a helpful personal assistant."},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=512,
    )

    answer = response.choices[0].message.content

    return jsonify({'answer': answer}), 200


@app.route("/summarize", methods=['POST'])
def summarize():

    email_text = request.form.get('email')

    prompt = f"Summarize the following email:\n{email_text}"

    response = groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Act like an expert email assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )

    summary = response.choices[0].message.content

    return jsonify({'summary': summary}), 200


if __name__ == "__main__":
    app.run()