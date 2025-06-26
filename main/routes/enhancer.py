from main.resume_enhancer import call_gemini_on
from flask import Blueprint, jsonify, render_template
import json

enhancer_bp = Blueprint('enhancer', __name__)

@enhancer_bp.route('/enhancer')
def enhance_resume():
    with open("uploads/resume.json") as f:
        data = json.load(f)

    enhanced = call_gemini_on(data["extracted_text"])

    data["enhanced_resume"] = enhanced

    with open("uploads/resume.json", "w", encoding = "utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return jsonify({"status":"done"})

@enhancer_bp.route('/enhanced')
def enhanced_resume():
    with open("uploads/resume.json") as f:
        data = json.load(f)

    enhanced_Resume = data.get("enhanced_resume", "No enhanced resume available.")

    return render_template("enhanced.html", enhanced_resume=enhanced_Resume)