from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask import send_from_directory
import os
import PyPDF2
import openai

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for all routes
print("Starting MedPrepare Flask App...")
# Configure OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        # Read PDF file
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return jsonify({"content": text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-content", methods=["POST"])
def generate_content():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate summary
        summary_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize the following text:\n{text}",
            max_tokens=150
        )
        summary = summary_response["choices"][0]["text"].strip()

        # Generate flashcards
        flashcards_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Create flashcards from the following text:\n{text}",
            max_tokens=300
        )
        flashcards = flashcards_response["choices"][0]["text"].strip()

        # Generate quiz
        quiz_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Create a quiz based on the following text:\n{text}",
            max_tokens=200
        )
        quiz = quiz_response["choices"][0]["text"].strip()

        return jsonify({
            "summary": summary,
            "flashcards": flashcards,
            "quiz": quiz
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)