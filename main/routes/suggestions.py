import json
from flask import Blueprint, render_template
from main.suggestions import get_course_recommendations

suggestions_bp = Blueprint('suggestions', __name__, url_prefix='/suggestions')


@suggestions_bp.route('/')
def show_suggestions():
    with open("./uploads/resume.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        tokens = data.get('tokens', [])

    recommendations = get_course_recommendations(tokens)
    
    return render_template('suggestions.html', recommendations = recommendations)