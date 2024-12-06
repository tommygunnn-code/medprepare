# backend/routes/pdf_routes.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from ..services.pdf_processing import extract_pdf_text
import os

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/upload", methods=["POST"])
def upload_pdf():
    """Handles PDF upload and text extraction."""
    # Check if file is in request
    if "file" not in request.files:
        current_app.logger.error("No file key found in request.")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        current_app.logger.error(f"Invalid file type: {file.filename}")
        return jsonify({"error": "Only PDF files are supported."}), 400

    # Secure the filename to prevent directory traversal attacks
    filename = secure_filename(file.filename)
    pages_param = request.args.get("pages")  # e.g., "0-2" or "0,2,4"

    try:
        # Extract text from the PDF
        current_app.logger.info(f"Processing file: {filename} with pages: {pages_param}")
        text = extract_pdf_text(file, pages_param)

        # Return extracted text
        current_app.logger.info(f"Successfully processed file: {filename}")
        return jsonify({"content": text}), 200
    except ValueError as ve:
        current_app.logger.warning(f"Value error while processing file {filename}: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error while processing file {filename}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
