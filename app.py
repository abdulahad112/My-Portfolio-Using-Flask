import os
import logging
import tempfile
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, current_app
from config import Config
from forms import ContactForm
from models import db, ContactMessage
from flask_migrate import Migrate
from flask_mail import Mail, Message

# ---------- Logging (early) ----------
logging.basicConfig(level=logging.INFO)

# ---------- App (create) ----------
app = Flask(__name__, instance_relative_config=True)

# ---------- SERVERLESS-SAFE: ensure instance_path is writable ----------
# Use FLASK_INSTANCE_PATH env var to override (set in Vercel or other host)
instance_path = os.environ.get("FLASK_INSTANCE_PATH", "/tmp/instance")

# On some platforms /tmp might not exist exactly like this; fallback to tempfile
if not instance_path:
    instance_path = os.path.join(tempfile.gettempdir(), "instance")

try:
    os.makedirs(instance_path, exist_ok=True)
    app.instance_path = instance_path
    logging.info(f"Using instance_path: {app.instance_path}")
except Exception as exc:
    # If creation fails (rare), log and continue — Flask will use default instance_path
    logging.warning(f"Could not set instance_path to {instance_path}: {exc}")

# ---------- Load config ----------
app.config.from_object(Config)

# ---------- Extensions (initialize once) ----------
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

mail = Mail()
mail.init_app(app)
@app.route('/')
def index():
    skills = [
        {'name': 'Python', 'pct': 80},
        {'name': 'Flask', 'pct': 80},
        {'name': 'Django', 'pct': 70},
        {'name': 'JavaScript', 'pct': 70},
        {'name': 'Bootstrap', 'pct': 90},
        {'name': 'Technical Writing', 'pct': 90},
        {'name': 'Machine Learning', 'pct': 75},
    ]
    projects = [
        {'title': 'Riskbeat (Heart Disease Risk Prediction System)', 'category': 'AI/ ML Website', 'desc': 'The project offers Role-Based Access Control (RBAC), ensuring distinct functionalities for Admin, Doctor, and User roles. It incorporates Machine Learning Models, including Gradient Boosting and Logistic Regression, to provide accurate health predictions. The User-Friendly Interface allows seamless navigation for submitting health data and viewing results. An integrated Doctor Search and Appointment Booking module enables users to find and schedule consultations with healthcare professionals. Additionally, the system includes a Feedback Collection mechanism to gather user suggestions for continuous improvement.', 'img':'main.png', 'github': 'https://github.com/abdulahad112/RiskBeat--Heart-Disease-Risk-Prediction-System'},
        {'title': 'Technical/Academic Writing Projects', 'category': 'Writing', 'desc': 'I specialize in crafting clear, concise, and well-researched technical and academic content, bridging the gap between complex concepts and accessible knowledge. My writing spans research papers, technical documentation, project reports, and data-driven analyses, with a strong emphasis on machine learning, healthcare technology, and software development. In my work, I prioritize precision, readability, and evidence-based reasoning, ensuring that technical details are presented logically for both expert and non-expert audiences. My experience includes writing research summaries, algorithm explanations, system documentation, and peer-reviewed academic content, often incorporating data visualizations, code snippets, and structured arguments to enhance clarity.', 'img':'techh.png', 'github': 'https://github.com/abdulahad112/Technical-Academic-Writing-Projects'},
        {'title': 'Software Piracy Protection', 'category': 'Python Software', 'desc': 'The Software Protection Application is a Python-based software developed by my and my group mates from Mirpur University of Science and Technology to safeguard digital products from piracy and unauthorized access, featuring an engaging welcome page with sound integration and an intuitive main menu offering options like "Protect Piracy," "Help," "Bug Report," "About Us," "Visit Us," and "Exit." The "Protect Piracy" section allows users to register software, pack files, and encrypt/decrypt data, while the "Help" page provides clear instructions, the "Bug Report" page facilitates issue reporting, and the "About Us" section shares project background and developer credits, with the "Visit Us" option linking to their LinkedIn profiles for further engagement, ensuring a user-friendly experience for software protection and support.', 'img':'intro.png', 'github': 'https://github.com/abdulahad112/Software-Piracy-Protection'},
          {
            'title': 'Talken AI Chatbot',
            'category': 'AI/ML',
            'desc': 'Talken Chatbot, Developed an AI-powered web chatbot using Flask and DeepSeek API, featuring a responsive UI with real-time messaging. Implemented secure environment configuration and session management while following Python best practices. Designed a clean frontend interface with HTML/CSS/JavaScript. Deployed with proper version control (Git) and dependency isolation (virtualenv). Has Features like, Save history, View History, Copy Message, Regenerate Message etc.',
            'img': 'Chatbot.png',
            'github': 'https://github.com/abdulahad112/Talken-Chatbot'
        },
        # New card 2
        {
            'title': 'Interactive-Dictionary with AI-Speech Recognition Using Python',
            'category': 'AI based GUI',
            'desc': 'Developed a Python dictionary app with AI speech recognition for voice-controlled word lookup, translation, and database management. Designed an intuitive GUI enabling users to add, update, and delete entries while maintaining SQLite/JSON data persistence. Implemented real-time speech-to-text processing using cutting-edge NLP libraries. Optimized search algorithms for millisecond response times with 95%+ speech recognition accuracy. Built as a modular system with OOP principles for easy feature expansion. Deployed with secure user authentication and encrypted local storage.',
            'img': 'dict.png',
            'github': 'https://github.com/abdulahad112/Interactive-Dictionary-with-AI-Speech-Recognition-Using-Python'
        }
    ]    
    
    
    return render_template('index.html', skills=skills, projects=projects)

@app.route('/projects')
def projects_page():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Save message to DB
        msg_entry = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(msg_entry)
        db.session.commit()

        try:
            msg = Message(
                subject="New Contact Form Submission",
                recipients=[app.config['ADMIN_EMAIL']],
                sender=app.config['MAIL_DEFAULT_SENDER'],
                body=f"Name: {form.name.data}\nEmail: {form.email.data}\nMessage:\n{form.message.data}"
            )
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            print(f"Email sending error: {e}")
            flash("Message saved but failed to send email (check SMTP settings).", "warning")

        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


@app.route('/download/resume')
def download_resume():
    folder = os.path.join(app.root_path, 'static', 'assets')
    return send_from_directory(folder, 'ahadcv.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)