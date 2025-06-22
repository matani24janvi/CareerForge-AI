from flask import Blueprint, jsonify, request, render_template, current_app
import os, json
from werkzeug.utils import secure_filename
from main.logger import event_logger, error_logger
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import glob
from main.preprocessing_logic import preprocessing_logic

resume_analyser_bp = Blueprint('resume_analyser', __name__, url_prefix='/resume_analyser')

# 🔍 Extraction Helpers

def extract_docx(path):
    doc = Document(path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_pdf(path):
    doc = fitz.open(path)
    return ''.join([page.get_text() for page in doc])

def extract_ocr(path):
    images = convert_from_path(path)
    return ''.join([pytesseract.image_to_string(img) for img in images])

@resume_analyser_bp.route('/', methods=['POST'])
def upload_resume():
    try:
        event_logger.info("Resume upload request received")

        if 'file' not in request.files:
            error_logger.warning("No file part in upload request")
            return jsonify({'success': False, 'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            error_logger.warning("No file selected in upload request")
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        allowed_extensions = {'pdf', 'doc', 'docx'}
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if ext not in allowed_extensions:
            error_logger.warning(f"Invalid file type uploaded: {ext}")
            return jsonify({'success': False, 'error': 'Invalid file type. Allowed: PDF, DOC, DOCX'}), 400

        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # 🧠 Extract Text Based on File Type
        extracted_text = ""
        if ext == 'docx' or ext == 'doc':
            extracted_text = extract_docx(filepath)
        elif ext == 'pdf':
            extracted_text = extract_pdf(filepath)

        # 📄 Fallback to OCR if text is empty
        if not extracted_text.strip() and ext == 'pdf':
            event_logger.info("Falling back to OCR for scanned PDF")
            extracted_text = extract_ocr(filepath)

        parsed_data = {'filename': filename, 'extracted_text': extracted_text.strip()}
        for ext in ('*.pdf', '*.docx', '*.doc', '*json'):
            for old_file in glob.glob(os.path.join(upload_folder, ext)):
                try:
                    os.remove(old_file)
                except Exception as e:
                    error_logger.error(f"Error deleting old file {old_file}: {str(e)}")
                    continue
        json_path = os.path.join(upload_folder, "resume.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        event_logger.info(f"Resume parsed successfully: {filename}")

        preprocessing_logic(json_path)

        return jsonify({
            'success': True,
            'message': 'Resume uploaded and parsed',
            'filename': filename,
            'text_preview': extracted_text[:500] + ('...' if len(extracted_text) > 500 else '')
        }), 200

    except Exception as e:
        error_logger.error(f"Error during resume processing: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Internal server error'}), 500