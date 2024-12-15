# backend/routes/pdf_routes.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from services.pdf_processing import extract_pdf_text
from services.openai_service import process_with_ai
import os
import json
import logging

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/upload", methods=["POST"])
def upload_pdf():
    """Handles PDF upload, text extraction, and AI processing."""
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
        extracted_text = extract_pdf_text(file, pages_param)
        current_app.logger.debug(f"Extracted text: {extracted_text[:500]}...")  # Log first 500 chars
        
        # Process the extracted text with OpenAI
        current_app.logger.info("Processing extracted text with AI...")
        ai_response = process_with_ai(extracted_text)
        current_app.logger.info(f"AI Response received: {ai_response}")
        
        # Parse the JSON response from OpenAI
        processed_content = json.loads(ai_response)
        current_app.logger.info(f"Parsed AI response: {json.dumps(processed_content, indent=2)}")
        
        # Return processed content
        response_data = {
            "raw_text": extracted_text,
            "processed_content": processed_content
        }
        current_app.logger.info(f"Sending response: {json.dumps(response_data, indent=2)}")
        
        return jsonify(response_data), 200
        
    except ValueError as ve:
        current_app.logger.warning(f"Value error while processing file {filename}: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected error while processing file {filename}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
