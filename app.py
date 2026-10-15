
# from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import pandas as pd
# import pickle
# import os
# import random
# import math

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safety.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Database Models
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     full_name = db.Column(db.String(100), nullable=False)
#     role = db.Column(db.String(20), default='user')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class GuardianRelation(db.Model):
#     __tablename__ = 'guardian_relation'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     relationship = db.Column(db.String(50))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', foreign_keys=[user_id], backref='guardian_relations')
#     guardian = db.relationship('User', foreign_keys=[guardian_id], backref='user_relations')

# class Alert(db.Model):
#     __tablename__ = 'alert'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     alert_type = db.Column(db.String(50))
#     risk_level = db.Column(db.Integer)
#     latitude = db.Column(db.Float)
#     longitude = db.Column(db.Float)
#     status = db.Column(db.String(20), default='active')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', backref='alerts')

# class Location(db.Model):
#     __tablename__ = 'location'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', backref='locations')

# class Feedback(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# # Create tables
# with app.app_context():
#     db.create_all()
#     print("✅ Database tables created")
    
#     # Create admin user if not exists
#     if not User.query.filter_by(username='admin').first():
#         admin = User(
#             username='admin',
#             email='admin@safety.com',
#             full_name='System Administrator',
#             phone='0000000000',
#             role='admin',
#             password_hash=generate_password_hash('admin123')
#         )
#         db.session.add(admin)
#         db.session.commit()
#         print("✅ Admin user created (admin/admin123)")
    
#     # Create test guardian if not exists
#     if not User.query.filter_by(username='testguardian').first():
#         guardian = User(
#             username='testguardian',
#             email='guardian@test.com',
#             full_name='Test Guardian',
#             phone='9876543211',
#             role='guardian',
#             password_hash=generate_password_hash('guardian123')
#         )
#         db.session.add(guardian)
#         db.session.commit()
#         print("✅ Test guardian created (testguardian/guardian123)")
    
#     # Create test user if not exists
#     if not User.query.filter_by(username='testuser').first():
#         testuser = User(
#             username='testuser',
#             email='test@test.com',
#             full_name='Test User',
#             phone='9876543210',
#             role='user',
#             password_hash=generate_password_hash('test123')
#         )
#         db.session.add(testuser)
#         db.session.commit()
#         print("✅ Test user created (testuser/test123)")
        
#         # Create guardian relation
#         guardian = User.query.filter_by(username='testguardian').first()
#         if guardian:
#             relation = GuardianRelation(
#                 user_id=testuser.id,
#                 guardian_id=guardian.id,
#                 relationship='Family Member'
#             )
#             db.session.add(relation)
#             db.session.commit()
#             print("✅ Guardian relation created")

# # Load ML Model
# try:
#     if os.path.exists("model.pkl") and os.path.exists("crime_dataset.csv"):
#         model = pickle.load(open("model.pkl", "rb"))
#         dataset = pd.read_csv("crime_dataset.csv")
#         print("✅ Model loaded")
#     else:
#         model = None
#         dataset = None
#         print("⚠️ Model files not found. Run python train_model.py")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     model = None
#     dataset = None

# # Helper function
# def is_logged_in():
#     return 'user_id' in session

# # Routes
# @app.route('/')
# def home():
#     user = None
#     if is_logged_in():
#         user = User.query.get(session['user_id'])
#     return render_template('home.html', user=user)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         full_name = request.form.get('full_name')
#         phone = request.form.get('phone')
#         role = request.form.get('role', 'user')
        
#         # Check if user exists
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists!', 'error')
#             return redirect(url_for('register'))
        
#         if User.query.filter_by(email=email).first():
#             flash('Email already registered!', 'error')
#             return redirect(url_for('register'))
        
#         # Create user
#         user = User(
#             username=username,
#             email=email,
#             full_name=full_name,
#             phone=phone,
#             role=role,
#             password_hash=generate_password_hash(password)
#         )
        
#         db.session.add(user)
#         db.session.commit()
        
#         flash('Registration successful! Please login.', 'success')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         role = request.form.get('role')
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and check_password_hash(user.password_hash, password) and user.role == role:
#             session['user_id'] = user.id
#             session['username'] = user.username
#             session['full_name'] = user.full_name
#             session['role'] = user.role
            
#             if user.role == 'user':
#                 return redirect(url_for('user_dashboard'))
#             elif user.role == 'guardian':
#                 return redirect(url_for('guardian_dashboard'))
#             else:
#                 return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Invalid username, password, or role mismatch!', 'error')
#             return redirect(url_for('login'))
    
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     flash('Logged out successfully!', 'success')
#     return redirect(url_for('home'))

# @app.route('/user')
# def user_dashboard():
#     if not is_logged_in():
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     if session.get('role') != 'user':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     user = User.query.get(session['user_id'])
#     guardians = GuardianRelation.query.filter_by(user_id=user.id).all()
#     recent_alerts = Alert.query.filter_by(user_id=user.id).order_by(Alert.created_at.desc()).limit(5).all()
    
#     # Get all guardians for dropdown
#     all_guardians = User.query.filter_by(role='guardian').all()
    
#     return render_template('user_dashboard.html', user=user, guardians=guardians, recent_alerts=recent_alerts, all_guardians=all_guardians)

# @app.route('/guardian')
# def guardian_dashboard():
#     if not is_logged_in():
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     if session.get('role') != 'guardian':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     user = User.query.get(session['user_id'])
#     monitored_users = GuardianRelation.query.filter_by(guardian_id=user.id).all()
    
#     return render_template('guardian_dashboard.html', user=user, monitored_users=monitored_users)

# @app.route('/admin')
# def admin_dashboard():
#     if not is_logged_in():
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     if session.get('role') != 'admin':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     users = User.query.all()
#     feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
#     alerts = Alert.query.order_by(Alert.created_at.desc()).limit(10).all()
#     guardian_relations = GuardianRelation.query.all()
    
#     return render_template('admin_dashboard.html', 
#                          user=User.query.get(session['user_id']), 
#                          users=users, 
#                          feedbacks=feedbacks, 
#                          alerts=alerts,
#                          guardian_relations=guardian_relations)

# @app.route('/save_location', methods=['POST'])
# def save_location():
#     if not is_logged_in():
#         return jsonify({'error': 'Not logged in'}), 401
    
#     data = request.get_json()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
    
#     if latitude and longitude:
#         location = Location(
#             user_id=session['user_id'],
#             latitude=latitude,
#             longitude=longitude
#         )
#         db.session.add(location)
#         db.session.commit()
        
#         # Check risk
#         risk = check_location_risk(latitude, longitude)
#         if risk > 70:
#             alert = Alert(
#                 user_id=session['user_id'],
#                 alert_type='auto',
#                 risk_level=risk,
#                 latitude=latitude,
#                 longitude=longitude,
#                 status='active'
#             )
#             db.session.add(alert)
#             db.session.commit()
        
#         return jsonify({'success': True, 'risk': risk})
    
#     return jsonify({'error': 'Invalid location'}), 400

# def check_location_risk(lat, lon):
#     """Simple risk calculation based on coordinates"""
#     # Risk zones in Mumbai
#     risk_zones = [
#         {'lat': 19.0760, 'lon': 72.8777, 'name': 'Andheri', 'risk': 85},
#         {'lat': 19.0596, 'lon': 72.8295, 'name': 'Bandra', 'risk': 45},
#         {'lat': 19.0759, 'lon': 72.8817, 'name': 'Kurla', 'risk': 75},
#         {'lat': 19.1176, 'lon': 72.9061, 'name': 'Powai', 'risk': 35},
#         {'lat': 19.0176, 'lon': 72.8561, 'name': 'Dadar', 'risk': 55},
#         {'lat': 19.2183, 'lon': 72.9781, 'name': 'Thane', 'risk': 30},
#     ]
    
#     for zone in risk_zones:
#         distance = math.sqrt((lat - zone['lat'])**2 + (lon - zone['lon'])**2) * 111
#         if distance < 3:
#             return zone['risk']
    
#     return random.randint(20, 50)

# @app.route('/get_location/<int:user_id>')
# def get_user_location(user_id):
#     if not is_logged_in():
#         return jsonify({'error': 'Not logged in'}), 401
    
#     location = Location.query.filter_by(user_id=user_id).order_by(Location.timestamp.desc()).first()
#     if location:
#         return jsonify({
#             'latitude': location.latitude,
#             'longitude': location.longitude,
#             'timestamp': location.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         })
#     return jsonify({'error': 'No location found'}), 404

# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if not is_logged_in():
#         flash('Please login to use safety check!', 'error')
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         area = request.form.get('area')
#         time_of_day = request.form.get('time')
        
#         if model and dataset is not None:
#             try:
#                 row = dataset[dataset['area'].str.lower() == area.lower()]
#                 if not row.empty:
#                     crime = int(row['crime_count'].values[0])
#                     night = 1 if time_of_day == 'night' else 0
#                     result = model.predict([[crime, night]])
#                     risk = model.predict_proba([[crime, night]])[0][1] * 100
                    
#                     if result[0] == 1:
#                         alert = Alert(
#                             user_id=session['user_id'],
#                             alert_type='auto',
#                             risk_level=int(risk),
#                             status='active'
#                         )
#                         db.session.add(alert)
#                         db.session.commit()
#                         return render_template('alert.html', risk=round(risk, 1), area=area)
#                     else:
#                         return render_template('safe.html', risk=round(risk, 1), area=area)
#             except Exception as e:
#                 print(f"Error: {e}")
        
#         return render_template('alert.html', risk=75, area=area)
    
#     return render_template('predict.html')

# @app.route('/help')
# def help_page():
#     user = None
#     if is_logged_in():
#         user = User.query.get(session['user_id'])
#     return render_template('help.html', user=user)

# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         message = request.form.get('message')
        
#         feedback = Feedback(
#             user_id=session['user_id'] if is_logged_in() else None,
#             name=name,
#             email=email,
#             message=message
#         )
#         db.session.add(feedback)
#         db.session.commit()
        
#         flash('Thank you for your feedback!', 'success')
#         return redirect(url_for('home'))
    
#     return render_template('feedback.html')

# @app.route('/profile')
# def profile():
#     if not is_logged_in():
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     user = User.query.get(session['user_id'])
#     return render_template('profile.html', user=user)

# @app.route('/add_guardian', methods=['POST'])
# def add_guardian():
#     if not is_logged_in() or session.get('role') != 'user':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     guardian_username = request.form.get('guardian_username')
#     relationship = request.form.get('relationship')
    
#     if not guardian_username:
#         flash('Please enter a guardian username!', 'error')
#         return redirect(url_for('user_dashboard'))
    
#     guardian = User.query.filter_by(username=guardian_username, role='guardian').first()
    
#     if not guardian:
#         flash(f'Guardian "{guardian_username}" not found! Make sure the username is correct and they are registered as a guardian.', 'error')
#         return redirect(url_for('user_dashboard'))
    
#     # Check if already added
#     existing = GuardianRelation.query.filter_by(
#         user_id=session['user_id'],
#         guardian_id=guardian.id
#     ).first()
    
#     if existing:
#         flash(f'Guardian "{guardian_username}" is already added!', 'warning')
#     else:
#         relation = GuardianRelation(
#             user_id=session['user_id'],
#             guardian_id=guardian.id,
#             relationship=relationship or 'Family Member'
#         )
#         db.session.add(relation)
#         db.session.commit()
#         flash(f'✅ Guardian "{guardian.full_name}" added successfully!', 'success')
    
#     return redirect(url_for('user_dashboard'))

# @app.route('/remove_guardian/<int:guardian_id>', methods=['POST'])
# def remove_guardian(guardian_id):
#     if not is_logged_in() or session.get('role') != 'user':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     relation = GuardianRelation.query.filter_by(
#         user_id=session['user_id'],
#         guardian_id=guardian_id
#     ).first()
    
#     if relation:
#         db.session.delete(relation)
#         db.session.commit()
#         flash('Guardian removed successfully!', 'success')
    
#     return redirect(url_for('user_dashboard'))

# @app.route('/panic', methods=['POST'])
# def panic():
#     if not is_logged_in():
#         return jsonify({'error': 'Not logged in'}), 401
    
#     data = request.get_json()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
    
#     alert = Alert(
#         user_id=session['user_id'],
#         alert_type='panic',
#         risk_level=95,
#         latitude=latitude,
#         longitude=longitude,
#         status='active'
#     )
#     db.session.add(alert)
#     db.session.commit()
    
#     # Notify all guardians (simulate)
#     guardians = GuardianRelation.query.filter_by(user_id=session['user_id']).all()
#     for g in guardians:
#         print(f"📱 Alert sent to guardian: {g.guardian.full_name}")
    
#     return jsonify({'success': True, 'alert_id': alert.id})

# @app.route('/get_guardians_list')
# def get_guardians_list():
#     if not is_logged_in():
#         return jsonify([])
    
#     guardians = User.query.filter_by(role='guardian').all()
#     return jsonify([{'username': g.username, 'full_name': g.full_name} for g in guardians])

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import pickle
import os
import math
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safety.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GuardianRelation(db.Model):
    __tablename__ = 'guardian_relation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    relationship = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='guardian_relations')
    guardian = db.relationship('User', foreign_keys=[guardian_id], backref='user_relations')

class Alert(db.Model):
    __tablename__ = 'alert'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alert_type = db.Column(db.String(50))
    risk_level = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_address = db.Column(db.String(500))
    trigger_word = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='active')
    notified_to_guardians = db.Column(db.Boolean, default=False)
    notified_to_police = db.Column(db.Boolean, default=False)
    notified_to_ngo = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='alerts')

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== POLICE STATIONS DATA ====================

# POLICE_STATIONS = [
#     {'name': 'Andheri Police Station', 'lat': 19.1196, 'lon': 72.8465, 'phone': '100', 'address': 'Andheri East, Mumbai', 'distance': 2.3},
#     {'name': 'Bandra Police Station', 'lat': 19.0596, 'lon': 72.8295, 'phone': '100', 'address': 'Bandra West, Mumbai', 'distance': 3.1},
#     {'name': 'Kurla Police Station', 'lat': 19.0759, 'lon': 72.8817, 'phone': '100', 'address': 'Kurla, Mumbai', 'distance': 1.8},
#     {'name': 'Powai Police Station', 'lat': 19.1176, 'lon': 72.9061, 'phone': '100', 'address': 'Powai, Mumbai', 'distance': 4.2},
#     {'name': 'Dadar Police Station', 'lat': 19.0176, 'lon': 72.8561, 'phone': '100', 'address': 'Dadar, Mumbai', 'distance': 5.5},
# ]
POLICE_STATIONS = [
    {'name': 'Andheri Police Station', 'lat': 19.1196, 'lon': 72.8465, 'phone': '100', 'address': 'Andheri East, Mumbai'},
    {'name': 'Bandra Police Station', 'lat': 19.0596, 'lon': 72.8295, 'phone': '100', 'address': 'Bandra West, Mumbai'},
    {'name': 'Kurla Police Station', 'lat': 19.0759, 'lon': 72.8817, 'phone': '100', 'address': 'Kurla, Mumbai'},
    {'name': 'Powai Police Station', 'lat': 19.1176, 'lon': 72.9061, 'phone': '100', 'address': 'Powai, Mumbai'},
    {'name': 'Dadar Police Station', 'lat': 19.0176, 'lon': 72.8561, 'phone': '100', 'address': 'Dadar, Mumbai'},
    {'name': 'Juhu Police Station', 'lat': 19.1010, 'lon': 72.8258, 'phone': '100', 'address': 'Juhu, Mumbai'},
    {'name': 'Vile Parle Police Station', 'lat': 19.0996, 'lon': 72.8496, 'phone': '100', 'address': 'Vile Parle, Mumbai'},
    {'name': 'Santacruz Police Station', 'lat': 19.0896, 'lon': 72.8426, 'phone': '100', 'address': 'Santacruz, Mumbai'},
    {'name': 'Goregaon Police Station', 'lat': 19.1696, 'lon': 72.8526, 'phone': '100', 'address': 'Goregaon, Mumbai'},
]

NGO_LIST = [
    {'name': 'Women Helpline', 'phone': '1091', 'email': 'womenhelpline@gov.in'},
    {'name': 'NGO HelpLine (181)', 'phone': '181', 'email': 'ngo.help@womensafety.org'},
    {'name': 'Sneha Foundation', 'phone': '9820467890', 'email': 'help@sneha.org'},
    {'name': 'Majlis Manch', 'phone': '9821234567', 'email': 'majlis@womensafety.com'},
]

# Create tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created")
    
    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@safety.com',
            full_name='Administrator',
            phone='0000000000',
            role='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")

# Load ML Model
try:
    if os.path.exists("model.pkl") and os.path.exists("crime_dataset.csv"):
        model = pickle.load(open("model.pkl", "rb"))
        dataset = pd.read_csv("crime_dataset.csv")
        print("✅ AI Model loaded")
    else:
        model = None
        dataset = None
except:
    model = None
    dataset = None

# ==================== HELPER FUNCTIONS ====================

def is_logged_in():
    return 'user_id' in session

def get_address_from_coords(lat, lon):
    areas = {
        (19.0760, 72.8777): 'Andheri, Mumbai',
        (19.0596, 72.8295): 'Bandra, Mumbai',
        (19.0759, 72.8817): 'Kurla, Mumbai',
        (19.1176, 72.9061): 'Powai, Mumbai',
        (19.0176, 72.8561): 'Dadar, Mumbai',
    }
    for (area_lat, area_lon), address in areas.items():
        distance = math.sqrt((lat - area_lat)**2 + (lon - area_lon)**2) * 111
        if distance < 5:
            return address
    return f"Lat: {lat:.6f}, Lon: {lon:.6f}"

# def find_nearby_police(lat, lon):
#     nearby = []
#     for station in POLICE_STATIONS:
#         distance = math.sqrt((lat - station['lat'])**2 + (lon - station['lon'])**2) * 111
#         if distance < 10:
#             station_copy = station.copy()
#             station_copy['distance'] = round(distance, 1)
#             nearby.append(station_copy)
#     return sorted(nearby, key=lambda x: x['distance'])[:3]
# def find_nearby_police(lat, lon):
#     nearby = []
#     for station in POLICE_STATIONS:
#         distance = math.sqrt((lat - station['lat'])**2 + (lon - station['lon'])**2) * 111
#         if distance < 10:
#             station_copy = station.copy()
#             station_copy['distance'] = round(distance, 1)
#             nearby.append(station_copy)
#     return sorted(nearby, key=lambda x: x['distance'])[:5]
def find_nearby_police(lat, lon):
    """Find nearest police stations within 10km"""
    nearby = []
    for station in POLICE_STATIONS:
        distance = math.sqrt((lat - station['lat'])**2 + (lon - station['lon'])**2) * 111
        if distance < 10:
            station_copy = station.copy()
            station_copy['distance'] = round(distance, 1)
            nearby.append(station_copy)
    return sorted(nearby, key=lambda x: x['distance'])[:5]

# def send_emergency_alert(user_id, alert_id, latitude, longitude):
#     """Send alerts to guardians, police, and NGOs"""
#     user = User.query.get(user_id)
#     alert = Alert.query.get(alert_id)
    
#     if not user or not alert:
#         return None
    
#     location_address = get_address_from_coords(latitude, longitude) if latitude else "Location unknown"
#     nearby_police = find_nearby_police(latitude, longitude) if latitude else []
    
#     result = {
#         'guardian_names': [],
#         'guardian_details': [],
#         'police_names': [],
#         'police_details': [],
#         'ngo_names': [],
#         'ngo_details': []
#     }
    
#     print("\n" + "="*60)
#     print(f"🚨 EMERGENCY ALERT - {alert.alert_type.upper()}")
#     print(f"👤 User: {user.full_name} ({user.username})")
#     print(f"📍 Location: {location_address}")
#     print("="*60)
    
#     # 1. Notify Guardians
#     guardians = GuardianRelation.query.filter_by(user_id=user_id).all()
#     print(f"\n👨‍👩‍👧 GUARDIANS NOTIFIED ({len(guardians)}):")
#     for relation in guardians:
#         guardian = relation.guardian
#         print(f"   ✓ {guardian.full_name} ({guardian.phone}) - {relation.relationship}")
#         result['guardian_names'].append(guardian.full_name)
#         result['guardian_details'].append({
#             'name': guardian.full_name,
#             'phone': guardian.phone,
#             'relationship': relation.relationship
#         })
    
#     # 2. Notify Police
#     print(f"\n👮 POLICE STATIONS NOTIFIED ({len(nearby_police)}):")
#     for police in nearby_police:
#         print(f"   ✓ {police['name']} - {police['distance']} km - {police['phone']}")
#         result['police_names'].append(police['name'])
#         result['police_details'].append({
#             'name': police['name'],
#             'phone': police['phone'],
#             'distance': police['distance'],
#             'address': police['address']
#         })
    
#     # 3. Notify NGOs
#     print(f"\n🆘 NGOS NOTIFIED ({len(NGO_LIST)}):")
#     for ngo in NGO_LIST:
#         print(f"   ✓ {ngo['name']} - {ngo['phone']}")
#         result['ngo_names'].append(ngo['name'])
#         result['ngo_details'].append({
#             'name': ngo['name'],
#             'phone': ngo['phone'],
#             'email': ngo['email']
#         })
    
#     print("\n" + "="*60)
#     print("✅ ALL EMERGENCY SERVICES NOTIFIED")
#     print("="*60 + "\n")
    
#     return result
# def send_emergency_alert(user_id, alert_id, latitude, longitude):
#     """Send alerts to guardians, police, and NGOs"""
#     user = User.query.get(user_id)
#     alert = Alert.query.get(alert_id)
    
#     if not user or not alert:
#         return None
    
#     location_address = get_address_from_coords(latitude, longitude) if latitude else "Location unknown"
#     nearby_police = find_nearby_police(latitude, longitude) if latitude else []
    
#     result = {
#         'guardian_names': [],
#         'guardian_details': [],
#         'police_names': [],
#         'police_details': [],
#         'ngo_names': [],
#         'ngo_details': []
#     }
    
#     print("\n" + "="*60)
#     print(f"🚨 EMERGENCY ALERT - {alert.alert_type.upper()}")
#     print(f"👤 User: {user.full_name} ({user.username})")
#     print(f"📍 Location: {location_address}")
#     print("="*60)
    
#     # 1. Notify Guardians
#     guardians = GuardianRelation.query.filter_by(user_id=user_id).all()
#     print(f"\n👨‍👩‍👧 GUARDIANS NOTIFIED ({len(guardians)}):")
#     for relation in guardians:
#         guardian = relation.guardian
#         print(f"   ✓ {guardian.full_name} ({guardian.phone}) - {relation.relationship}")
#         result['guardian_names'].append(guardian.full_name)
#         result['guardian_details'].append({
#             'name': guardian.full_name,
#             'phone': guardian.phone,
#             'relationship': relation.relationship
#         })
    
#     # 2. Notify Police with distances
#     print(f"\n👮 POLICE STATIONS NOTIFIED ({len(nearby_police)}):")
#     for police in nearby_police:
#         print(f"   ✓ {police['name']} - {police['distance']} km away - {police['phone']}")
#         result['police_names'].append(f"{police['name']} ({police['distance']} km)")
#         result['police_details'].append({
#             'name': police['name'],
#             'phone': police['phone'],
#             'distance': police['distance'],
#             'address': police['address']
#         })
    
#     # 3. Notify NGOs
#     print(f"\n🆘 NGOS NOTIFIED ({len(NGO_LIST)}):")
#     for ngo in NGO_LIST:
#         print(f"   ✓ {ngo['name']} - {ngo['phone']}")
#         result['ngo_names'].append(ngo['name'])
#         result['ngo_details'].append({
#             'name': ngo['name'],
#             'phone': ngo['phone'],
#             'email': ngo['email']
#         })
    
#     print("\n" + "="*60)
#     print("✅ ALL EMERGENCY SERVICES NOTIFIED")
#     print("="*60 + "\n")
    
#     return result
def send_emergency_alert(user_id, alert_id, latitude, longitude):
    """Send alerts to guardians, police, and NGOs"""
    user = User.query.get(user_id)
    alert = Alert.query.get(alert_id)
    
    if not user or not alert:
        return None
    
    location_address = get_address_from_coords(latitude, longitude) if latitude else "Location unknown"
    nearby_police = find_nearby_police(latitude, longitude) if latitude else []
    
    result = {
        'guardian_names': [],
        'guardian_details': [],
        'police_names': [],
        'police_details': [],
        'ngo_names': [],
        'ngo_details': []
    }
    
    print("\n" + "="*60)
    print(f"🚨 EMERGENCY ALERT - {alert.alert_type.upper()}")
    print(f"👤 User: {user.full_name} ({user.username})")
    print(f"📍 Location: {location_address}")
    print("="*60)
    
    # 1. Notify Guardians
    guardians = GuardianRelation.query.filter_by(user_id=user_id).all()
    print(f"\n👨‍👩‍👧 GUARDIANS NOTIFIED ({len(guardians)}):")
    for relation in guardians:
        guardian = relation.guardian
        print(f"   ✓ {guardian.full_name} ({guardian.phone}) - {relation.relationship}")
        result['guardian_names'].append(guardian.full_name)
        result['guardian_details'].append({
            'name': guardian.full_name,
            'phone': guardian.phone,
            'relationship': relation.relationship
        })
    
    # 2. Notify Police - FIXED: Add police names properly
    print(f"\n👮 POLICE STATIONS NOTIFIED ({len(nearby_police)}):")
    for police in nearby_police:
        police_display = f"{police['name']} ({police['distance']} km)"
        print(f"   ✓ {police_display}")
        result['police_names'].append(police_display)  # Add to array for frontend
        result['police_details'].append({
            'name': police['name'],
            'phone': police['phone'],
            'distance': police['distance'],
            'address': police.get('address', 'Mumbai')
        })
    
    # 3. Notify NGOs
    print(f"\n🆘 NGOS NOTIFIED ({len(NGO_LIST)}):")
    for ngo in NGO_LIST:
        print(f"   ✓ {ngo['name']} - {ngo['phone']}")
        result['ngo_names'].append(ngo['name'])
        result['ngo_details'].append({
            'name': ngo['name'],
            'phone': ngo['phone'],
            'email': ngo['email']
        })
    
    print("\n" + "="*60)
    print("✅ ALL EMERGENCY SERVICES NOTIFIED")
    print(f"   Guardians: {len(result['guardian_names'])} notified")
    print(f"   Police: {len(result['police_names'])} stations notified")
    print(f"   NGOs: {len(result['ngo_names'])} organizations notified")
    print("="*60 + "\n")
    
    return result

# ==================== ROUTES ====================

@app.route('/')
def home():
    user = None
    if is_logged_in():
        user = User.query.get(session['user_id'])
    return render_template('home.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        role = request.form.get('role', 'user')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone,
            role=role,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password) and user.role == role:
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['role'] = user.role
            
            if user.role == 'user':
                return redirect(url_for('user_dashboard'))
            elif user.role == 'guardian':
                return redirect(url_for('guardian_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/user')
def user_dashboard():
    if not is_logged_in() or session.get('role') != 'user':
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    guardians = GuardianRelation.query.filter_by(user_id=user.id).all()
    recent_alerts = Alert.query.filter_by(user_id=user.id).order_by(Alert.created_at.desc()).limit(5).all()
    
    return render_template('user_dashboard.html', user=user, guardians=guardians, recent_alerts=recent_alerts)

@app.route('/guardian')
def guardian_dashboard():
    if not is_logged_in() or session.get('role') != 'guardian':
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    monitored_users = GuardianRelation.query.filter_by(guardian_id=user.id).all()
    
    # Get alerts for all monitored users
    user_ids = [rel.user_id for rel in monitored_users]
    recent_alerts = Alert.query.filter(Alert.user_id.in_(user_ids)).order_by(Alert.created_at.desc()).all() if user_ids else []
    
    return render_template('guardian_dashboard.html', user=user, monitored_users=monitored_users, recent_alerts=recent_alerts)

@app.route('/admin')
def admin_dashboard():
    if not is_logged_in() or session.get('role') != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('login'))
    
    users = User.query.all()
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    guardian_relations = GuardianRelation.query.all()
    
    return render_template('admin_dashboard.html', 
                         user=User.query.get(session['user_id']), 
                         users=users, 
                         alerts=alerts, 
                         feedbacks=feedbacks,
                         guardian_relations=guardian_relations)

@app.route('/save_location', methods=['POST'])
def save_location():
    if not is_logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude and longitude:
        location = Location(
            user_id=session['user_id'],
            latitude=latitude,
            longitude=longitude,
            address=get_address_from_coords(latitude, longitude)
        )
        db.session.add(location)
        db.session.commit()
        return jsonify({'success': True, 'risk': random.randint(20, 80)})
    
    return jsonify({'error': 'Invalid location'}), 400

@app.route('/voice_detect', methods=['POST'])
def voice_detect():
    data = request.get_json()
    text = data.get('text', '').lower()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    print(f"🔊 Voice detected: '{text}'")
    
    if is_logged_in():
        address = get_address_from_coords(latitude, longitude) if latitude and longitude else "Location unknown"
        
        alert = Alert(
            user_id=session['user_id'],
            alert_type='voice',
            risk_level=90,
            latitude=latitude,
            longitude=longitude,
            location_address=address,
            trigger_word=text,
            status='active'
        )
        db.session.add(alert)
        db.session.commit()
        
        notification_result = send_emergency_alert(session['user_id'], alert.id, latitude, longitude)
        
        return jsonify({
            'alert': True,
            'trigger': text,
            'notification': notification_result
        })
    
    return jsonify({'alert': False, 'require_login': True})

@app.route('/sos_pattern', methods=['POST'])
def sos_pattern():
    data = request.get_json()
    pattern = data.get('pattern')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    print(f"📱 SOS pattern detected: {pattern}")
    
    if pattern == 'shake' and is_logged_in():
        address = get_address_from_coords(latitude, longitude) if latitude and longitude else "Location unknown"
        
        alert = Alert(
            user_id=session['user_id'],
            alert_type='sos_pattern',
            risk_level=85,
            latitude=latitude,
            longitude=longitude,
            location_address=address,
            status='active'
        )
        db.session.add(alert)
        db.session.commit()
        
        notification_result = send_emergency_alert(session['user_id'], alert.id, latitude, longitude)
        
        return jsonify({'alert': True, 'notification': notification_result})
    
    return jsonify({'alert': False})

@app.route('/panic', methods=['POST'])
def panic():
    if not is_logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    print(f"🚨 Panic button triggered by user {session['user_id']}")
    
    address = get_address_from_coords(latitude, longitude) if latitude and longitude else "Location unknown"
    
    alert = Alert(
        user_id=session['user_id'],
        alert_type='panic',
        risk_level=95,
        latitude=latitude,
        longitude=longitude,
        location_address=address,
        status='active'
    )
    db.session.add(alert)
    db.session.commit()
    
    notification_result = send_emergency_alert(session['user_id'], alert.id, latitude, longitude)
    
    return jsonify({'success': True, 'alert_id': alert.id, 'notification': notification_result})

@app.route('/nearby_police')
def nearby_police():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat and lon:
        stations = find_nearby_police(lat, lon)
        return jsonify(stations)
    return jsonify(POLICE_STATIONS)

@app.route('/nearby_ngos')
def nearby_ngos():
    return jsonify(NGO_LIST)

@app.route('/resolve_alert/<int:alert_id>', methods=['POST'])
def resolve_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if alert:
        alert.status = 'resolved'
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Alert not found'}), 404

@app.route('/add_guardian', methods=['POST'])
def add_guardian():
    if not is_logged_in() or session.get('role') != 'user':
        flash('Access denied!', 'error')
        return redirect(url_for('home'))
    
    guardian_username = request.form.get('guardian_username')
    relationship = request.form.get('relationship')
    
    guardian = User.query.filter_by(username=guardian_username, role='guardian').first()
    
    if not guardian:
        flash(f'Guardian "{guardian_username}" not found!', 'error')
        return redirect(url_for('user_dashboard'))
    
    existing = GuardianRelation.query.filter_by(
        user_id=session['user_id'],
        guardian_id=guardian.id
    ).first()
    
    if existing:
        flash(f'Guardian already added!', 'warning')
    else:
        relation = GuardianRelation(
            user_id=session['user_id'],
            guardian_id=guardian.id,
            relationship=relationship or 'Family Member'
        )
        db.session.add(relation)
        db.session.commit()
        flash(f'✅ Guardian "{guardian.full_name}" added!', 'success')
    
    return redirect(url_for('user_dashboard'))

@app.route('/remove_guardian/<int:guardian_id>', methods=['POST'])
def remove_guardian(guardian_id):
    if not is_logged_in() or session.get('role') != 'user':
        flash('Access denied!', 'error')
        return redirect(url_for('home'))
    
    relation = GuardianRelation.query.filter_by(
        user_id=session['user_id'],
        guardian_id=guardian_id
    ).first()
    
    if relation:
        db.session.delete(relation)
        db.session.commit()
        flash('Guardian removed!', 'success')
    
    return redirect(url_for('user_dashboard'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if not is_logged_in():
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        area = request.form.get('area')
        time_of_day = request.form.get('time')
        risk = random.randint(20, 95)
        
        if risk > 60:
            return render_template('alert.html', risk=risk, area=area)
        else:
            return render_template('safe.html', risk=risk, area=area)
    
    return render_template('predict.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        feedback = Feedback(
            user_id=session['user_id'] if is_logged_in() else None,
            name=name,
            email=email,
            message=message
        )
        db.session.add(feedback)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('home'))
    
    return render_template('feedback.html')

@app.route('/profile')
def profile():
    if not is_logged_in():
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)













# from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import pandas as pd
# import pickle
# import os
# import math
# import random

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safety.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # ==================== DATABASE MODELS ====================

# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     full_name = db.Column(db.String(100), nullable=False)
#     role = db.Column(db.String(20), default='user')
#     is_verified = db.Column(db.Boolean, default=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class GuardianRelation(db.Model):
#     __tablename__ = 'guardian_relation'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     relationship = db.Column(db.String(50))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', foreign_keys=[user_id], backref='guardian_relations')
#     guardian = db.relationship('User', foreign_keys=[guardian_id], backref='user_relations')

# class Alert(db.Model):
#     __tablename__ = 'alert'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     alert_type = db.Column(db.String(50))
#     risk_level = db.Column(db.Integer)
#     latitude = db.Column(db.Float)
#     longitude = db.Column(db.Float)
#     location_address = db.Column(db.String(500))
#     trigger_word = db.Column(db.String(100), nullable=True)
#     status = db.Column(db.String(20), default='active')
#     notified_to_guardians = db.Column(db.Boolean, default=False)
#     notified_to_police = db.Column(db.Boolean, default=False)
#     notified_to_ngo = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', backref='alerts')

# class Location(db.Model):
#     __tablename__ = 'location'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     address = db.Column(db.String(500))
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# class Feedback(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     rating = db.Column(db.Integer, default=5)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# # ==================== POLICE STATIONS DATA ====================

# POLICE_STATIONS = [
#     {'name': 'Andheri Police Station', 'lat': 19.1196, 'lon': 72.8465, 'phone': '100', 'address': 'Andheri East, Mumbai'},
#     {'name': 'Bandra Police Station', 'lat': 19.0596, 'lon': 72.8295, 'phone': '100', 'address': 'Bandra West, Mumbai'},
#     {'name': 'Kurla Police Station', 'lat': 19.0759, 'lon': 72.8817, 'phone': '100', 'address': 'Kurla, Mumbai'},
#     {'name': 'Powai Police Station', 'lat': 19.1176, 'lon': 72.9061, 'phone': '100', 'address': 'Powai, Mumbai'},
#     {'name': 'Dadar Police Station', 'lat': 19.0176, 'lon': 72.8561, 'phone': '100', 'address': 'Dadar, Mumbai'},
#     {'name': 'Juhu Police Station', 'lat': 19.1010, 'lon': 72.8258, 'phone': '100', 'address': 'Juhu, Mumbai'},
#     {'name': 'Vile Parle Police Station', 'lat': 19.0996, 'lon': 72.8496, 'phone': '100', 'address': 'Vile Parle, Mumbai'},
#     {'name': 'Santacruz Police Station', 'lat': 19.0896, 'lon': 72.8426, 'phone': '100', 'address': 'Santacruz, Mumbai'},
#     {'name': 'Goregaon Police Station', 'lat': 19.1696, 'lon': 72.8526, 'phone': '100', 'address': 'Goregaon, Mumbai'},
# ]

# NGO_LIST = [
#     {'name': 'Women Helpline', 'phone': '1091', 'email': 'womenhelpline@gov.in'},
#     {'name': 'NGO HelpLine (181)', 'phone': '181', 'email': 'ngo.help@womensafety.org'},
#     {'name': 'Sneha Foundation', 'phone': '9820467890', 'email': 'help@sneha.org'},
#     {'name': 'Majlis Manch', 'phone': '9821234567', 'email': 'majlis@womensafety.com'},
# ]

# # Create tables
# with app.app_context():
#     db.create_all()
#     print("✅ Database tables created")
    
#     # Create admin user
#     if not User.query.filter_by(username='admin').first():
#         admin = User(
#             username='admin',
#             email='admin@safety.com',
#             full_name='Administrator',
#             phone='0000000000',
#             role='admin',
#             password_hash=generate_password_hash('admin123')
#         )
#         db.session.add(admin)
#         db.session.commit()
#         print("✅ Admin user created")

# # Load ML Model
# try:
#     if os.path.exists("model.pkl") and os.path.exists("crime_dataset.csv"):
#         model = pickle.load(open("model.pkl", "rb"))
#         dataset = pd.read_csv("crime_dataset.csv")
#         print("✅ AI Model loaded")
#     else:
#         model = None
#         dataset = None
# except:
#     model = None
#     dataset = None

# # ==================== HELPER FUNCTIONS ====================

# def is_logged_in():
#     return 'user_id' in session

# def get_address_from_coords(lat, lon):
#     areas = {
#         (19.0760, 72.8777): 'Andheri, Mumbai',
#         (19.0596, 72.8295): 'Bandra, Mumbai',
#         (19.0759, 72.8817): 'Kurla, Mumbai',
#         (19.1176, 72.9061): 'Powai, Mumbai',
#         (19.0176, 72.8561): 'Dadar, Mumbai',
#     }
#     for (area_lat, area_lon), address in areas.items():
#         distance = math.sqrt((lat - area_lat)**2 + (lon - area_lon)**2) * 111
#         if distance < 5:
#             return address
#     return f"Lat: {lat:.6f}, Lon: {lon:.6f}"

# def find_nearby_police(lat, lon):
#     """Find nearest police stations within 10km"""
#     nearby = []
#     for station in POLICE_STATIONS:
#         distance = math.sqrt((lat - station['lat'])**2 + (lon - station['lon'])**2) * 111
#         if distance < 10:
#             station_copy = station.copy()
#             station_copy['distance'] = round(distance, 1)
#             nearby.append(station_copy)
#     return sorted(nearby, key=lambda x: x['distance'])[:5]

# def send_emergency_alert(user_id, alert_id, latitude, longitude):
#     """Send alerts to guardians, police, and NGOs"""
#     user = User.query.get(user_id)
#     alert = Alert.query.get(alert_id)
    
#     if not user or not alert:
#         return None
    
#     location_address = get_address_from_coords(latitude, longitude) if latitude else "Location unknown"
#     nearby_police = find_nearby_police(latitude, longitude) if latitude else []
    
#     result = {
#         'guardian_names': [],
#         'guardian_details': [],
#         'police_names': [],
#         'police_details': [],
#         'ngo_names': [],
#         'ngo_details': []
#     }
    
#     print("\n" + "="*60)
#     print(f"🚨 EMERGENCY ALERT - {alert.alert_type.upper()}")
#     print(f"👤 User: {user.full_name} ({user.username})")
#     print(f"📍 Location: {location_address}")
#     print("="*60)
    
#     # 1. Notify Guardians
#     guardians = GuardianRelation.query.filter_by(user_id=user_id).all()
#     print(f"\n👨‍👩‍👧 GUARDIANS NOTIFIED ({len(guardians)}):")
#     for relation in guardians:
#         guardian = relation.guardian
#         print(f"   ✓ {guardian.full_name} ({guardian.phone}) - {relation.relationship}")
#         result['guardian_names'].append(guardian.full_name)
#         result['guardian_details'].append({
#             'name': guardian.full_name,
#             'phone': guardian.phone,
#             'relationship': relation.relationship
#         })
    
#     # 2. Notify Police - FIXED: Add police names properly
#     print(f"\n👮 POLICE STATIONS NOTIFIED ({len(nearby_police)}):")
#     for police in nearby_police:
#         police_display = f"{police['name']} ({police['distance']} km)"
#         print(f"   ✓ {police_display}")
#         result['police_names'].append(police_display)  # Add to array for frontend
#         result['police_details'].append({
#             'name': police['name'],
#             'phone': police['phone'],
#             'distance': police['distance'],
#             'address': police.get('address', 'Mumbai')
#         })
    
#     # 3. Notify NGOs
#     print(f"\n🆘 NGOS NOTIFIED ({len(NGO_LIST)}):")
#     for ngo in NGO_LIST:
#         print(f"   ✓ {ngo['name']} - {ngo['phone']}")
#         result['ngo_names'].append(ngo['name'])
#         result['ngo_details'].append({
#             'name': ngo['name'],
#             'phone': ngo['phone'],
#             'email': ngo['email']
#         })
    
#     print("\n" + "="*60)
#     print("✅ ALL EMERGENCY SERVICES NOTIFIED")
#     print(f"   Guardians: {len(result['guardian_names'])} notified")
#     print(f"   Police: {len(result['police_names'])} stations notified")
#     print(f"   NGOs: {len(result['ngo_names'])} organizations notified")
#     print("="*60 + "\n")
    
#     return result

# # ==================== ROUTES ====================

# @app.route('/')
# def home():
#     user = None
#     if is_logged_in():
#         user = User.query.get(session['user_id'])
#     return render_template('home.html', user=user)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         full_name = request.form.get('full_name')
#         phone = request.form.get('phone')
#         role = request.form.get('role', 'user')
        
#         if User.query.filter_by(username=username).first():
#             flash('Username already exists!', 'error')
#             return redirect(url_for('register'))
        
#         if User.query.filter_by(email=email).first():
#             flash('Email already registered!', 'error')
#             return redirect(url_for('register'))
        
#         user = User(
#             username=username,
#             email=email,
#             full_name=full_name,
#             phone=phone,
#             role=role,
#             password_hash=generate_password_hash(password)
#         )
#         db.session.add(user)
#         db.session.commit()
        
#         flash('Registration successful! Please login.', 'success')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         role = request.form.get('role')
        
#         user = User.query.filter_by(username=username).first()
        
#         if user and check_password_hash(user.password_hash, password) and user.role == role:
#             session['user_id'] = user.id
#             session['username'] = user.username
#             session['full_name'] = user.full_name
#             session['role'] = user.role
            
#             if user.role == 'user':
#                 return redirect(url_for('user_dashboard'))
#             elif user.role == 'guardian':
#                 return redirect(url_for('guardian_dashboard'))
#             else:
#                 return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Invalid credentials!', 'error')
#             return redirect(url_for('login'))
    
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     flash('Logged out successfully!', 'success')
#     return redirect(url_for('home'))

# @app.route('/user')
# def user_dashboard():
#     if not is_logged_in() or session.get('role') != 'user':
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     user = User.query.get(session['user_id'])
#     guardians = GuardianRelation.query.filter_by(user_id=user.id).all()
#     recent_alerts = Alert.query.filter_by(user_id=user.id).order_by(Alert.created_at.desc()).limit(5).all()
    
#     return render_template('user_dashboard.html', user=user, guardians=guardians, recent_alerts=recent_alerts)

# @app.route('/guardian')
# def guardian_dashboard():
#     if not is_logged_in() or session.get('role') != 'guardian':
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     user = User.query.get(session['user_id'])
#     monitored_users = GuardianRelation.query.filter_by(guardian_id=user.id).all()
    
#     # Get alerts for all monitored users
#     user_ids = [rel.user_id for rel in monitored_users]
#     recent_alerts = Alert.query.filter(Alert.user_id.in_(user_ids)).order_by(Alert.created_at.desc()).all() if user_ids else []
    
#     return render_template('guardian_dashboard.html', user=user, monitored_users=monitored_users, recent_alerts=recent_alerts)

# @app.route('/admin')
# def admin_dashboard():
#     if not is_logged_in() or session.get('role') != 'admin':
#         flash('Access denied!', 'error')
#         return redirect(url_for('login'))
    
#     users = User.query.all()
#     alerts = Alert.query.order_by(Alert.created_at.desc()).all()
#     feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
#     guardian_relations = GuardianRelation.query.all()
    
#     return render_template('admin_dashboard.html', 
#                          user=User.query.get(session['user_id']), 
#                          users=users, 
#                          alerts=alerts, 
#                          feedbacks=feedbacks,
#                          guardian_relations=guardian_relations)

# @app.route('/save_location', methods=['POST'])
# def save_location():
#     if not is_logged_in():
#         return jsonify({'error': 'Not logged in'}), 401
    
#     data = request.get_json()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
    
#     if latitude and longitude:
#         location = Location(
#             user_id=session['user_id'],
#             latitude=latitude,
#             longitude=longitude,
#             address=get_address_from_coords(latitude, longitude)
#         )
#         db.session.add(location)
#         db.session.commit()
#         return jsonify({'success': True, 'risk': random.randint(20, 80)})
    
#     return jsonify({'error': 'Invalid location'}), 400

# @app.route('/voice_detect', methods=['POST'])
# def voice_detect():
#     data = request.get_json()
#     text = data.get('text', '').lower()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
    
#     print(f"🔊 Voice detected: '{text}'")
    
#     if is_logged_in():
#         address = get_address_from_coords(latitude, longitude) if latitude and longitude else "Location unknown"
        
#         alert = Alert(
#             user_id=session['user_id'],
#             alert_type='voice',
#             risk_level=90,
#             latitude=latitude,
#             longitude=longitude,
#             location_address=address,
#             trigger_word=text,
#             status='active'
#         )
#         db.session.add(alert)
#         db.session.commit()
        
#         notification_result = send_emergency_alert(session['user_id'], alert.id, latitude, longitude)
        
#         return jsonify({
#             'alert': True,
#             'trigger': text,
#             'notification': notification_result
#         })
    
#     return jsonify({'alert': False, 'require_login': True})

# @app.route('/sos_pattern', methods=['POST'])
# def sos_pattern():
#     data = request.get_json()
#     pattern = data.get('pattern')
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
    
#     print(f"📱 SOS pattern detected: {pattern}")
    
#     if pattern == 'shake' and is_logged_in():
#         address = get_address_from_coords(latitude, longitude) if latitude and longitude else "Location unknown"
        
#         alert = Alert(
#             user_id=session['user_id'],
#             alert_type='sos_pattern',
#             risk_level=85,
#             latitude=latitude,
#             longitude=longitude,
#             location_address=address,
#             status='active'
#         )
#         db.session.add(alert)
#         db.session.commit()
        
#         notification_result = send_emergency_alert(session['user_id'], alert.id, latitude, longitude)
        
#         return jsonify({'alert': True, 'notification': notification_result})
    
#     return jsonify({'alert': False})

# @app.route('/panic', methods=['POST'])
# def panic():
#     if not is_logged_in():
#         return jsonify({'error': 'Not logged in'}), 401
    
#     data = request.get_json()
#     latitude = data.get('latitude')
#     longitude = data.get('longitude')
    
#     print(f"🚨 Panic button triggered by user {session['user_id']}")
    
#     address = get_address_from_coords(latitude, longitude) if latitude and longitude else "Location unknown"
    
#     alert = Alert(
#         user_id=session['user_id'],
#         alert_type='panic',
#         risk_level=95,
#         latitude=latitude,
#         longitude=longitude,
#         location_address=address,
#         status='active'
#     )
#     db.session.add(alert)
#     db.session.commit()
    
#     notification_result = send_emergency_alert(session['user_id'], alert.id, latitude, longitude)
    
#     return jsonify({'success': True, 'alert_id': alert.id, 'notification': notification_result})

# @app.route('/nearby_police')
# def nearby_police():
#     lat = request.args.get('lat', type=float)
#     lon = request.args.get('lon', type=float)
    
#     if lat and lon:
#         stations = find_nearby_police(lat, lon)
#         return jsonify(stations)
#     return jsonify(POLICE_STATIONS)

# @app.route('/nearby_ngos')
# def nearby_ngos():
#     return jsonify(NGO_LIST)

# @app.route('/resolve_alert/<int:alert_id>', methods=['POST'])
# def resolve_alert(alert_id):
#     alert = Alert.query.get(alert_id)
#     if alert:
#         alert.status = 'resolved'
#         db.session.commit()
#         return jsonify({'success': True})
#     return jsonify({'error': 'Alert not found'}), 404

# @app.route('/add_guardian', methods=['POST'])
# def add_guardian():
#     if not is_logged_in() or session.get('role') != 'user':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     guardian_username = request.form.get('guardian_username')
#     relationship = request.form.get('relationship')
    
#     guardian = User.query.filter_by(username=guardian_username, role='guardian').first()
    
#     if not guardian:
#         flash(f'Guardian "{guardian_username}" not found!', 'error')
#         return redirect(url_for('user_dashboard'))
    
#     existing = GuardianRelation.query.filter_by(
#         user_id=session['user_id'],
#         guardian_id=guardian.id
#     ).first()
    
#     if existing:
#         flash(f'Guardian already added!', 'warning')
#     else:
#         relation = GuardianRelation(
#             user_id=session['user_id'],
#             guardian_id=guardian.id,
#             relationship=relationship or 'Family Member'
#         )
#         db.session.add(relation)
#         db.session.commit()
#         flash(f'✅ Guardian "{guardian.full_name}" added!', 'success')
    
#     return redirect(url_for('user_dashboard'))

# @app.route('/remove_guardian/<int:guardian_id>', methods=['POST'])
# def remove_guardian(guardian_id):
#     if not is_logged_in() or session.get('role') != 'user':
#         flash('Access denied!', 'error')
#         return redirect(url_for('home'))
    
#     relation = GuardianRelation.query.filter_by(
#         user_id=session['user_id'],
#         guardian_id=guardian_id
#     ).first()
    
#     if relation:
#         db.session.delete(relation)
#         db.session.commit()
#         flash('Guardian removed!', 'success')
    
#     return redirect(url_for('user_dashboard'))

# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if not is_logged_in():
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         area = request.form.get('area')
#         time_of_day = request.form.get('time')
#         risk = random.randint(20, 95)
        
#         if risk > 60:
#             return render_template('alert.html', risk=risk, area=area)
#         else:
#             return render_template('safe.html', risk=risk, area=area)
    
#     return render_template('predict.html')

# @app.route('/help')
# def help_page():
#     return render_template('help.html')

# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         message = request.form.get('message')
        
#         feedback = Feedback(
#             user_id=session['user_id'] if is_logged_in() else None,
#             name=name,
#             email=email,
#             message=message
#         )
#         db.session.add(feedback)
#         db.session.commit()
        
#         flash('Thank you for your feedback!', 'success')
#         return redirect(url_for('home'))
    
#     return render_template('feedback.html')

# @app.route('/profile')
# def profile():
#     if not is_logged_in():
#         flash('Please login first!', 'error')
#         return redirect(url_for('login'))
    
#     user = User.query.get(session['user_id'])
#     return render_template('profile.html', user=user)

# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5000)