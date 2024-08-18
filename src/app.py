from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.user_profile import user_profile_bp

app = Flask(__name__)

# Configuration for SQLAlchemy and JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///curatehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# For testing purposes, I have kept the key publicly available
app.config['JWT_SECRET_KEY'] = b'\xe8\xb1\xb9\xcc\xd3i\xa6\x15\xf2\xe2/j\xd0\x1d\xfe\xb2M\xc7(\x1e\x11\xb0\xa3\xb9'

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    preferences = db.Column(db.String(500), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Activity Log model
class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ActivityLog {self.username} - {self.action}>'

# Home route
@app.route('/')
def home():
    return "Welcome to CurateHub!"

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 201

# User profile update
@app.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.get_json()
    preferences = data.get('preferences')

    user = User.query.filter_by(username=current_user).first()
    if user:
        user.preferences = preferences
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

# Get user profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if user:
        return jsonify({"username": user.username, "email": user.email, "preferences": user.preferences}), 200
    return jsonify({"error": "User not found"}), 404

# GET method for recommendations
@app.route('/api/recommendations', methods=['GET'])
def get_recommendations_get():
    interests = request.args.getlist('interests')
    search_keyword = request.args.get('search', '')
    recommendations = [
        {"title": f"Recommended video for {interest} 1"} for interest in interests
    ]
    return jsonify({'recommendations': recommendations})

# POST method for recommendations
@app.route('/api/recommendations', methods=['POST'])
def get_recommendations_post():
    data = request.json
    interest = data.get('interest')
    search_keyword = data.get('search', '')
    recommendations = [
        {"title": f"Recommended video for {interest} 1"},
        {"title": f"Recommended video for {interest} 2"}
    ]
    filtered_recommendations = [rec for rec in recommendations if search_keyword.lower() in rec['title'].lower()]
    return jsonify({"recommendations": filtered_recommendations})

# Log user activity
@app.route('/log_activity', methods=['POST'])
@jwt_required()
def log_activity():
    current_user = get_jwt_identity()
    data = request.get_json()
    action = data.get('action')

    log = ActivityLog(username=current_user, action=action)
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Activity logged successfully"}), 201

# Get user analytics
@app.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    current_user = get_jwt_identity()
    logs = ActivityLog.query.filter_by(username=current_user).all()
    analytics = [{"action": log.action, "timestamp": log.timestamp} for log in logs]
    return jsonify({"analytics": analytics}), 200

# Test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'GET method works!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database tables
    app.run(debug=True)

# Register the blueprint
app.register_blueprint(user_profile_bp)
