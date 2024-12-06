from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai
import pymupdf4llm

app = Flask(__name__, static_folder="static")
CORS(app)
print("Starting MedPrepare Flask App...")

# Load environment variables
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
        # Save the file temporarily to work with it
        file_path = os.path.join("temp", file.filename)
        os.makedirs("temp", exist_ok=True)
        file.save(file_path)

        # Use pymupdf4llm to extract text as markdown
        md_text = pymupdf4llm.to_markdown(file_path)

        # Clean up temporary file
        os.remove(file_path)

        return jsonify({"content": md_text}), 200
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
