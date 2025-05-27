from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ericwriter.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

AVAILABLE_THEMES = [
    "minimalist",
    "cyberpunk",
    "beach_vacation",
    "major_city",
    "outer_space",
    "custom"
]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(20), nullable=False, default='minimalist')
    custom_font_size = db.Column(db.Integer, default=16)
    custom_bg_primary = db.Column(db.String(7), default='#ffffff')
    custom_bg_secondary = db.Column(db.String(7), default='#ffffff')
    custom_text_primary = db.Column(db.String(7), default='#000000')
    custom_text_secondary = db.Column(db.String(7), default='#000000')
    custom_accent_color = db.Column(db.String(7), default='#000000')
    documents = db.relationship('Document', backref='author', lazy=True)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        user = User(
            username=data['username'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True})
    return render_template('register.html')

@app.route('/api/documents', methods=['GET', 'POST'])
@login_required
def documents():
    if request.method == 'POST':
        data = request.get_json()
        doc = Document(
            title=data.get('title', 'Untitled'),
            content=data['content'],
            user_id=current_user.id
        )
        db.session.add(doc)
        db.session.commit()
        return jsonify({'success': True, 'id': doc.id})
    
    docs = Document.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': doc.id,
        'title': doc.title,
        'content': doc.content,
        'updated_at': doc.updated_at
    } for doc in docs])

@app.route('/api/documents/<int:doc_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if request.method == 'GET':
        return jsonify({
            'id': doc.id,
            'title': doc.title,
            'content': doc.content
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        doc.title = data.get('title', doc.title)
        doc.content = data.get('content', doc.content)
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(doc)
        db.session.commit()
        return jsonify({'success': True})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        data = request.get_json()
        if 'theme' in data and data['theme'] in AVAILABLE_THEMES:
            current_user.theme = data['theme']
            db.session.commit()
            return jsonify({'success': True})
        elif 'custom_settings' in data:
            # Update custom theme settings
            current_user.custom_font_size = data['custom_settings'].get('font_size', 16)
            current_user.custom_bg_primary = data['custom_settings'].get('bg_primary', '#ffffff')
            current_user.custom_bg_secondary = data['custom_settings'].get('bg_secondary', '#ffffff')
            current_user.custom_text_primary = data['custom_settings'].get('text_primary', '#000000')
            current_user.custom_text_secondary = data['custom_settings'].get('text_secondary', '#000000')
            current_user.custom_accent_color = data['custom_settings'].get('accent_color', '#000000')
            current_user.theme = 'custom'
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid request'})
    
    custom_settings = {
        'font_size': current_user.custom_font_size,
        'bg_primary': current_user.custom_bg_primary,
        'bg_secondary': current_user.custom_bg_secondary,
        'text_primary': current_user.custom_text_primary,
        'text_secondary': current_user.custom_text_secondary,
        'accent_color': current_user.custom_accent_color
    }
    
    return render_template('settings.html', themes=AVAILABLE_THEMES, current_theme=current_user.theme, custom_settings=custom_settings)

@app.route('/api/current_theme')
@login_required
def get_current_theme():
    custom_settings = None
    if current_user.theme == 'custom':
        custom_settings = {
            'font_size': current_user.custom_font_size,
            'bg_primary': current_user.custom_bg_primary,
            'bg_secondary': current_user.custom_bg_secondary,
            'text_primary': current_user.custom_text_primary,
            'text_secondary': current_user.custom_text_secondary,
            'accent_color': current_user.custom_accent_color
        }
    return jsonify({'theme': current_user.theme, 'custom_settings': custom_settings})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 