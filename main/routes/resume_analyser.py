from flask import Blueprint, jsonify, request, render_template, current_app
import os
from werkzeug.utils import secure_filename
from main.logger import event_logger, error_logger

resume_analyser_bp = Blueprint('resume_analyser', __name__, url_prefix='/resume_analyser')

@resume_analyser_bp.route('/ping')
def ping():
    event_logger.info("resume_analyser ping endpoint called")
    return jsonify({'success': True, 'message': 'pong'})

@resume_analyser_bp.route('/')
def upload_form():
    event_logger.info("Upload form page accessed")
    return render_template('index.html')

@resume_analyser_bp.route('/upload', methods=['POST'])
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
        
        allowed_extensions = {'pdf', 'doc', 'docx', 'txt'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            error_logger.warning(f"Invalid file type uploaded: {file_extension}")
            return jsonify({'success': False, 'error': 'Invalid file type. Allowed: PDF, DOC, DOCX, TXT'}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        event_logger.info(f"Resume uploaded successfully: {filename}")
        
        return jsonify({
            'success': True, 
            'message': 'Resume uploaded successfully',
            'filename': filename,
            'filepath': filepath
        }), 200
        
    except Exception as e:
        error_logger.error(f"Error during resume upload: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
