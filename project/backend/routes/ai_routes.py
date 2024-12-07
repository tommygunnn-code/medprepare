from flask import Blueprint, request, jsonify
from ..services.openai_service import process_with_ai

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/process", methods=["POST"])
def process_content():
    data = request.json
    content = data.get("content")
    
    if not content:
        return jsonify({"error": "No content provided"}), 400
        
    try:
        result = process_with_ai(content)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500