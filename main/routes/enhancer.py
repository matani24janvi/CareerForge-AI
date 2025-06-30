from flask import Blueprint, jsonify, render_template, send_from_directory
from main.resume_enhancer import call_gemini_on
from markdown_pdf import MarkdownPdf, Section
import json, os

enhancer_bp = Blueprint('enhancer', __name__)
UPLOAD_FOLDER = "uploads"
PDF_FILENAME = "enhanced_resume.pdf"
JSON_FILENAME = "resume.json"

# Route: Enhance the resume and generate a PDF
@enhancer_bp.route('/enhancer')
def enhance_resume():
    with open(os.path.join(UPLOAD_FOLDER, JSON_FILENAME), "r", encoding="utf-8") as f:
        data = json.load(f)

    enhanced_md = call_gemini_on(data.get("extracted_text", ""))
    data["enhanced_resume"] = enhanced_md

    with open(os.path.join(UPLOAD_FOLDER, JSON_FILENAME), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    css = """ 
    body { font-family: 'Segoe UI', sans-serif; padding: 2rem; line-height: 1.6; }
    h1, h2, h3 { color: #2c3e50; }
    ul { margin-left: 1.5rem; }
    table, th, td { border: 1px solid #999; border-collapse: collapse; padding: 8px; }
    """

    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(enhanced_md), user_css=css)
    pdf.meta["title"] = "Enhanced Resume"
    pdf.meta["author"] = "CareerForge AI"
    pdf.save(os.path.join(UPLOAD_FOLDER, PDF_FILENAME))

    return jsonify({"status": "done"})

# Route: Render enhanced resume HTML page
@enhancer_bp.route('/enhanced')
def view_enhanced_resume():
    with open(os.path.join(UPLOAD_FOLDER, JSON_FILENAME), "r", encoding="utf-8") as f:
        data = json.load(f)
    return render_template("enhanced.html")

# Route: Serve PDF file directly
@enhancer_bp.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    uploads_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    return send_from_directory(uploads_path, filename)
