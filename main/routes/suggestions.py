import json
from flask import Blueprint, render_template
from main.suggestions import get_course_recommendations

suggestions_bp = Blueprint('suggestions', __name__, url_prefix='/suggestions')


@suggestions_bp.route('/')
def show_suggestions():
    with open("./uploads/resume.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        tokens = data.get('tokens', [])

    get_course_recommendations(tokens)

    resume_data = json.load(open("./uploads/resume.json", 'r', encoding='utf-8'))
    
    return render_template('suggestions.html', data = resume_data)