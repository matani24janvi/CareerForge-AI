from flask import Blueprint, render_template, redirect, url_for

complementary_bp = Blueprint('complementary', __name__)

@complementary_bp.route('/about')
def about():
    return render_template('about.html')

@complementary_bp.route('/contact')
def contact():
    return render_template('contact.html')

@complementary_bp.route('/help')
def help():
    return render_template('help.html')

@complementary_bp.route('/work')
def work():
    return render_template('work.html')


