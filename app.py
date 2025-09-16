import os
from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
from flask_mail import Mail, Message


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')


# Mail configuration (optional) - set environment variables in production
app.config.update(
    MAIL_SERVER='smtp.gmail.com',  # Gmail SMTP server
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='nikhil_kumar@cmr.edu.in',
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD', ''),  # Set this via environment variable
    MAIL_DEFAULT_SENDER='nikhil_kumar@cmr.edu.in'
)
mail = Mail(app)


# Data (you can move this to a JSON or DB later)
skills = [
{"name": "Python", "level": 90, "logo": "images/python.jpg", "years": 4},
{"name": "Flask", "level": 88, "logo": "images/flask.jpg", "years": 3},
{"name": "SQL", "level": 82, "logo": "images/sql.jpg", "years": 3},
{"name": "HTML/CSS", "level": 95, "logo": "images/html.jpg", "years": 5},
{"name": "JavaScript", "level": 80, "logo": "images/js.jpg", "years": 3},
{"name": "Data Analysis", "level": 86, "logo": "images/data.jpg", "years": 3}
]


projects = [
    {
        "id": 1,
        "title": "Smart Task Manager",
        "description": "Full-stack task manager with user auth, REST API and Postgres.",
        "images": [
            "images/Screenshot 2025-09-16 164553.png",
            "images/Screenshot 2025-09-16 165141.png",
            "images/Screenshot 2025-09-16 165237.png"
        ],
        "link": "https://aiportfolio-1.onrender.com/",  # Updated live demo link
        "repo": "https://aiportfolio-1.onrender.com/",  # Updated repo link
        "tags": ["Flask", "Postgres", "Docker"]
    },
    {
        "id": 2,
        "title": "AI Portfolio Generator",
        "description": "An AI-powered portfolio website generator using OpenAI's GPT model.",
        "images": ["images/project 2.png"],  # Removed Nerd_NIkhil.png
        "link": "https://aiportfolio-1.onrender.com/",
        "repo": "https://github.com/Nerd-Nikhil/aiportfolio",
        "tags": ["Python", "OpenAI", "Flask", "Render"]
    }
]


resume_file = 'resume.pdf' # put resume.pdf under static/


@app.route('/')
def index():
    return render_template('index.html', skills=skills, projects=projects, resume=resume_file)


@app.route('/download-resume')
def download_resume():
    return send_from_directory(os.path.join(app.static_folder), resume_file, as_attachment=True)


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    if not (name and email and message):
        flash('Please fill all fields', 'danger')
        return redirect(url_for('index') + '#contact')

    # send email if mail server configured
    try:
        if app.config.get('MAIL_USERNAME'):
            msg = Message(subject=f'Portfolio Contact from {name}', recipients=[app.config.get('MAIL_DEFAULT_SENDER')])
            msg.body = f'From: {name} <{email}>\n\n{message}'
            mail.send(msg)
        flash('Message sent! I will get back to you shortly.', 'success')
    except Exception as e:
        app.logger.exception('Mail send failed')
        flash('Could not send message (server configuration). It was logged locally.', 'warning')
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)