from main.resume_enhancer import call_gemini_on
from flask import Blueprint, jsonify, render_template
import json

enhancer_bp = Blueprint('enhancer', __name__, url_prefix='/enhancer')

@enhancer_bp.route('/')
def show_enhanced_resume():
    with open("uploads/resume.json") as f:
        data = json.load(f)
    enhanced = call_gemini_on(data["extracted_text"])
    return jsonify(enhanced)