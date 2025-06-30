from main.resume_enhancer import call_gemini_on
from flask import Blueprint, jsonify, render_template
import json
from markdown_pdf import MarkdownPdf, Section

enhancer_bp = Blueprint('enhancer', __name__)

@enhancer_bp.route('/enhancer')
def enhance_resume():
    with open("uploads/resume.json") as f:
        data = json.load(f)

    enhanced_md = call_gemini_on(data["extracted_text"])

    data["enhanced_resume"] = enhanced_md
    with open("uploads/resume.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    css = """ 
    body { font-family: 'Segoe UI', sans-serif; padding: 2rem; line-height: 1.6; }
    h1, h2, h3 { color: #2c3e50; }
    ul { margin-left: 1.5rem; }
    table, th, td { border: 1px solid #999; border-collapse: collapse; padding: 8px; }
    """

    pdf = MarkdownPdf(toc_level=2, optimize = True)
    pdf.add_section(Section(enhanced_md), user_css = css)
    pdf.meta["title"] = "Enhanced Resume"
    pdf.meta["author"] = "CareerForge AI"
    pdf.save("uploads/enhanced_resume.pdf")

    return jsonify({"status":"done"})

@enhancer_bp.route('/enhanced')
def enhanced_resume():
    with open("uploads/resume.json") as f:
        data = json.load(f)

    enhanced_Resume = data.get("enhanced_resume", "No enhanced resume available.")

    return render_template("enhanced.html", enhanced_resume=enhanced_Resume)