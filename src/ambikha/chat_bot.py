from flask import Flask, render_template, request, jsonify
import os
import ai_demo
import currency_api

print("Setting up ChromaDB...")
collection = ai_demo.setup_chromadb()

ai_demo.load_chroma_data(collection)
print("\nEnsure Ollama is running locally with at least one model downloaded.")
print(
    "You can start Ollama and download the llama2 model with: 'ollama run llama2'\n"
)

app = Flask(__name__, template_folder="templates")

if not os.path.exists("templates"):
    os.makedirs("templates")

if not os.path.exists("static"):
    os.makedirs("static")

with open("templates/index.html", "r") as f:
    html_content = f.read()

responses = {}

default_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "Interesting. Tell me more about that.",
    "I'm still learning. Could you try asking something else?",
    "I don't have an answer for that yet.",
    "Let's talk about something else. What's on your mind?",
]


def get_response(user_input):
    user_input = user_input.lower()
    response = ai_demo.submit_ai_query(user_input, collection)
    formatted_response = format_response(response)
    if not formatted_response:
        return "I don't understand"
    return formatted_response


def format_response(text):
    if len(text) < 80:
        return text

    words = text.split()
    paragraphs = []
    current_paragraph = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > 80 and current_length > 50:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = [word]
            current_length = len(word)
        else:
            current_paragraph.append(word)
            current_length += len(word) + 1  # +1 for the space

    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    return "\n\n".join(paragraphs)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot_response = get_response(user_message).replace("• ", "").split(". ")
    bot_response = ". \n".join(bot_response)
    return jsonify({"response": bot_response})


if __name__ == "__main__":
    print("Chatbot is starting up...")
    print("Make sure you have Flask installed. If not, run: pip install flask")
    print("To interact with the chatbot, open your web browser and go to:")
    print("http://127.0.0.1:5000/")
    app.run(debug=True)
