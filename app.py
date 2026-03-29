import os
import smtplib
from functools import wraps
from datetime import datetime
from email.mime.text import MIMEText
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'campus_retain_super_secret_hackathon_key'

# --- CONFIG ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_retain.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# EMAIL SETUP
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = "vishvanth193049@gmail.com" 
MAIL_PASSWORD = "Life@789" # 16-character App Password

db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    location = db.Column(db.String(100))
    secret_detail = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Available')
    date_found = db.Column(db.DateTime, default=datetime.utcnow)
    claims = db.relationship('Claim', backref='item', lazy=True, cascade="all, delete-orphan")

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    student_id = db.Column(db.String(50))
    student_email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    proof_description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def send_email(receiver, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = MAIL_USERNAME
    msg['To'] = receiver
    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Mail Error: {e}")
        return False

# --- DECORATORS ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') != True:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- AUTH ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email.endswith('@alliance.edu.in'):
            return render_template('login.html', error="Only @alliance.edu.in organization emails are allowed.")

        user = User.query.filter_by(email=email).first()

        # Hackathon auto-register feature if new email in organization domain
        if not user:
            new_user = User(email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['user_email'] = email
            return redirect(url_for('index'))
        else:
            if check_password_hash(user.password, password):
                session['user_email'] = email
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error="Incorrect password.")

    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Hardcoded Admin credentials for MVP
        if email == 'admin@alliance.edu.in' and password == 'admin123':
            session['is_admin'] = True
            session['user_email'] = email
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid Admin Credentials.")

    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- MAIN ROUTES ---

@app.route('/')
@login_required
def index():
    user_email = session.get('user_email')
    items = Item.query.filter(Item.status.in_(['Available', 'Pending'])).order_by(Item.date_found.desc()).all()
    return render_template('index.html', items=items, user_email=user_email)

@app.route('/admin')
@admin_required
def admin_dashboard():
    items = Item.query.order_by(Item.date_found.desc()).all()
    return render_template('admin.html', items=items)

@app.route('/api/report', methods=['POST'])
@login_required
def report_item():
    try:
        f = request.files.get('image')
        fname = None
        if f and f.filename != '':
            fname = secure_filename(f"{datetime.now().timestamp()}_{f.filename}")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))

        new_item = Item(
            name=request.form['name'],
            category=request.form.get('category', 'Other'),
            location=request.form['location'],
            secret_detail=request.form.get('secret_detail', ''),
            image_path=fname
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/claim', methods=['POST'])
@login_required
def claim_item():
    try:
        data = request.json
        item = db.session.get(Item, data['item_id'])
        if item:
            item.status = 'Pending'
            send_email(data['student_email'], "Claim Received", f"We received your claim for {item.name}. Verification is in progress.")

        new_claim = Claim(
            item_id=data['item_id'],
            student_id=data['student_id'],
            student_email=data['student_email'],
            phone=data.get('phone', ''),
            proof_description=data['proof_description']
        )
        db.session.add(new_claim)
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/api/admin/approve/<int:item_id>', methods=['POST'])
@admin_required
def approve_claim(item_id):
    item = db.session.get(Item, item_id)
    if item:
        item.status = 'Claimed'
        latest = Claim.query.filter_by(item_id=item_id).order_by(Claim.timestamp.desc()).first()
        if latest:
            send_email(latest.student_email, "Item Ready", f"APPROVED! Please collect {item.name} from the Student Center.")
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

@app.route('/api/item/delete/<int:item_id>', methods=['POST'])
@admin_required
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    # Support for Zoho Catalyst and standard PaaS (Render/Heroku)
    port = int(os.environ.get('X_ZOHO_CATALYST_LISTEN_PORT', os.environ.get('PORT', 9000)))
    app.run(host='0.0.0.0', port=port, debug=False)
