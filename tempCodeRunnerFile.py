from flask import render_template
from main import create_app

app = create_app()

@app.route('/', methods=['GET','POST'])
def submit_resume():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)