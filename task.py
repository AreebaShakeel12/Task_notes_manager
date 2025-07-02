from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import json
import os
from datetime import datetime, date

# pip import Groq ---
from groq import Groq


# --- Load Configuration from config.json ---
with open(r'C:\Users\DELL\Desktop\flask\taskmanager\config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super secret key' # Consider moving this to config.json for production
app.config['UPLOAD_FOLDER'] = params['upload_location']

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD= params['gmail_password']
)
mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Database Models ---

class User(db.Model, UserMixin):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(2000), nullable=False)

    tasks = db.relationship('Task', backref='author', lazy=True, foreign_keys='[Task.user_id]')
    notess = db.relationship('Note', backref='author', lazy=True, foreign_keys='[Note.user_id]')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(20), default='Normal')
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.title}', '{self.due_date}', '{self.is_completed}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.title}', '{self.timestamp}')"

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('sigreg.html', username=username, email=email)
        
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Username already taken. Please choose a different one.', 'danger')
            return render_template('sigreg.html', username=username, email=email)
        if email_exists:
            flash('Email already registered. Please use a different email or login.', 'danger')
            return render_template('sigreg.html', username=username, email=email)

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('sigreg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return render_template('sigreg.html', email=email)

    return render_template('sigreg.html')

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()

    todays_tasks = Task.query.filter_by(user_id=current_user.id)\
        .filter(Task.due_date == today).order_by(Task.due_date.asc()).all()

    upcoming_tasks = Task.query.filter_by(user_id=current_user.id)\
        .filter(Task.due_date > today).order_by(Task.due_date.asc()).all()
    
    upcoming_notes = Note.query.filter_by(user_id=current_user.id)\
    .order_by(Note.timestamp.asc()).all()

    completed_tasks = Task.query.filter_by(user_id=current_user.id, is_completed=True).count()
    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.timestamp.desc()).all()

    return render_template(
        'dashboard.html',
        user=current_user,
        todays_tasks=todays_tasks,
        upcoming_tasks=upcoming_tasks,
        upcoming_notes=upcoming_notes,
        notes=notes,
        progress=progress
    )

# --- TASKS ROUTES (CRUD Operations) ---
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks_page():
    if request.method == 'POST':
        title = request.form.get('title')
        due_date_str = request.form.get('due_date')
        priority = request.form.get('priority', 'Normal')

        if not title:
            flash('Task title cannot be empty.', 'danger')
            return redirect(url_for('tasks_page'))

        due_date_obj = None
        if due_date_str:
            try:
                due_date_obj = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format for due date. Please use YYYY-MM-DD.', 'danger')
                return redirect(url_for('tasks_page'))

        new_task = Task(
            title=title,
            due_date=due_date_obj,
            priority=priority,
            user_id=current_user.id,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_task)
        db.session.commit()
       
        return redirect(url_for('tasks_page'))
    
    sort_param = request.args.get('sort', 'added_date_desc')

    tasks_query = Task.query.filter_by(user_id=current_user.id)

    if sort_param == 'added_date_desc':
        tasks_query = tasks_query.order_by(Task.timestamp.desc())
    elif sort_param == 'added_date_asc':
        tasks_query = tasks_query.order_by(Task.timestamp.asc())
    elif sort_param == 'due_date_asc':
        tasks_query = tasks_query.order_by(Task.due_date.asc().nulls_last())
    elif sort_param == 'due_date_desc':
        tasks_query = tasks_query.order_by(Task.due_date.desc().nulls_first())

    all_tasks = tasks_query.all()
    return render_template('task.html', all_tasks=all_tasks, current_date=date.today())

@app.route('/update_task_completion/<int:task_id>', methods=['POST'])
@login_required
def update_task_completion(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify(success=False, message='Task not found'), 404

    if task.user_id != current_user.id:
        return jsonify(success=False, message='Unauthorized'), 403

    data = request.get_json()
    task.is_completed = data.get('is_completed', False)
    db.session.commit()

    return jsonify(success=True)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks_page'))

    if task.user_id != current_user.id:
        flash('You are not authorized to edit this task.', 'danger')
        return redirect(url_for('tasks_page'))
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        due_date_str = request.form.get('due_date')
        task.priority = request.form.get('priority', 'Normal')
        task.is_completed = 'is_completed' in request.form
        
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format for due date. Please use YYYY-MM-DD.', 'danger')
                return render_template('edit_task.html', task=task)
        else:
            task.due_date = None
        
        db.session.commit()
       
        return redirect(url_for('tasks_page'))
    
    return render_template('edit_task.html', task=task)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        flash('Task not found.', 'danger')
        return redirect(url_for('tasks_page'))

    if task.user_id != current_user.id:
        flash('You are not authorized to delete this task.', 'danger')
        return redirect(url_for('tasks_page'))
    
    db.session.delete(task)
    db.session.commit()
    
    return redirect(url_for('tasks_page'))

# --- NOTES ROUTES ---
@app.route('/notes', methods=['GET'])
@login_required
def notes_page():
    notes_query = Note.query.filter_by(user_id=current_user.id)
    all_notes = notes_query.order_by(Note.timestamp.desc()).all()
    return render_template('notes.html', all_notes=all_notes)

@app.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Note title and content cannot be empty.', 'danger')
            return redirect(url_for('add_note'))
        
        new_note = Note(
            title=title,
            content=content,
            user_id=current_user.id,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_note)
        db.session.commit()
        
        return redirect(url_for('notes_page')) 
    return render_template('add_note.html')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        flash('Note not found.', 'danger')
        return redirect(url_for('notes_page'))
    if note.user_id != current_user.id:
        flash('You are not authorized to edit this note.', 'danger')
        return redirect(url_for('notes_page'))
    
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')

        if not note.title or not note.content:
            flash('Note title and content cannot be empty.', 'danger')
            return render_template('edit_note.html', note=note)
        
        db.session.commit()
       
        return redirect(url_for('notes_page'))
    
    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>', methods=['POST','GET'])
@login_required
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note.user_id != current_user.id:
        return jsonify(success=False, message='Unauthorized'), 403
    
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes_page'))


# ... (snip) ...

try:
    groq_client = Groq(api_key=params['GROQ_API_KEY'])
except KeyError:
    print("Error: 'GROQ_API_KEY' not found in config.json params.")
    groq_client = None # Handle case where key is missing

@app.route('/api/summarize_note', methods=['POST'])
@login_required
def summarize_note_api():
    if not groq_client:
        return jsonify({"error": "Groq API is not configured. Please check GROQ_API_KEY in config.json."}), 500

    data = request.get_json()
    note_content = data.get('content', '')

    if not note_content:
        return jsonify({"error": "No content provided for summarization."}), 400

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    # MODIFIED PROMPT:
                    "content": f"Provide a concise summary with key points highlighting important aspects of the following text. Do not include any introductory phrases like 'Here is a summary:' or 'Based on the text:'. Just provide the summary:\n\n{note_content}",
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=250,
        )

        if chat_completion.choices and chat_completion.choices[0].message and chat_completion.choices[0].message.content:
            summary = chat_completion.choices[0].message.content
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": "Failed to generate summary. No text found in AI response."}), 500
    except Exception as e:
        print(f"Error calling Groq API: {e}") # This print will show in your Flask terminal
        return jsonify({"error": f"An error occurred during summarization: {str(e)}"}), 500
    
@app.route('/summery')
@login_required
def summery_page():
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.timestamp.desc()).all()
    return render_template('summery.html', notes=notes, user=current_user)


# --- Database Creation (Run this once on startup) ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Creates tables if they don't exist
    app.run(debug=True)