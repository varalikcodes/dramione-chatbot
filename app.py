from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# System prompt for Dramione chatbot
system_prompt = """
You are a fanfiction assistant specialized in Draco and Hermione (Dramione) fanfiction.
All your responses must stay within the Dramione universe.
Use settings such as Hogwarts, the war, the Room of Requirement, the Malfoy Manor, the library, etc.
Your tone must match the Dramione genre: emotionally complex, romantic, occasionally tense or witty.
Include references to common Dramione tropes, and speak like a normal person.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"reply": "I need something to respond to, love. Even Malfoy has better conversation than silence."})

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
            messages=messages,
            temperature=0.8
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        # Log the actual error in the backend logs for debugging
        print(f"🔴 Error communicating with OpenAI: {str(e)}")
        return jsonify({
            "reply": "Something went wrong. Maybe a rogue Niffler got into the server?"
        })

if __name__ == "__main__":
    app.run(debug=True)
