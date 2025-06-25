from flask import Blueprint, render_template

loader_bp = Blueprint('loader', __name__, url_prefix='/loader')

@loader_bp.route('/process')
def show_process_loader():
    return render_template('load1.html')


@loader_bp.route('/enhance')
def show_enhance_loader():
    return render_template('load2.html')