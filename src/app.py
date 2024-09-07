from flask import Flask, jsonify, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS
import logging
from bson import ObjectId

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = b'`\xc8\xe7C5\xc3\x13wE\xe4\xf0\xba\x8cM\xfeW\x0e\x87O6\x87\xbaP\x9f'

# Configuration for MongoDB and JWT
app.config['MONGO_URI'] = 'mongodb://localhost:27017/curatehub'
app.config['JWT_SECRET_KEY'] = b'\xe8\xb1\xb9\xcc\xd3i\xa6\x15\xf2\xe2/j\xd0\x1d\xfe\xb2M\xc7(\x1e\x11\xb0\xa3\xb9'
mongo = PyMongo(app)
db = mongo.db  # This will give you access to the database

# Initialize extensions
mongo = PyMongo(app)
jwt = JWTManager(app)

# Initialize CORS
CORS(app)

# Define MongoDB collections
users = mongo.db.users
activity_logs = mongo.db.activity_logs
categories = mongo.db.categories
tags = mongo.db.tags
contents = mongo.db.contents

# Route to create a new category
@app.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    name = data.get('name')

    if categories.find_one({'name': name}):
        return jsonify({"error": "Category already exists"}), 400

    categories.insert_one({'name': name})
    return jsonify({"message": "Category created successfully"}), 201

# Route to get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    all_categories = categories.find()
    return jsonify([{"id": str(cat['_id']), "name": cat['name']} for cat in all_categories])

# Route to create a new tag
@app.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    data = request.get_json()
    name = data.get('name')

    if tags.find_one({'name': name}):
        return jsonify({"error": "Tag already exists"}), 400

    tags.insert_one({'name': name})
    return jsonify({"message": "Tag created successfully"}), 201

# Route to get all tags
@app.route('/tags', methods=['GET'])
def get_tags():
    all_tags = tags.find()
    return jsonify([{"id": str(tag['_id']), "name": tag['name']} for tag in all_tags])

# Route to associate content with a category
@app.route('/content/<content_id>/category/<category_id>', methods=['PUT'])
@jwt_required()
def associate_content_with_category(content_id, category_id):
    content = contents.find_one({'_id': content_id})
    category = categories.find_one({'_id': category_id})
    
    if not content or not category:
        return jsonify({"error": "Content or Category not found"}), 404

    contents.update_one({'_id': content_id}, {'$set': {'category': category_id}})
    return jsonify({"message": "Content associated with category successfully"}), 200

# Route to associate tags with content
@app.route('/content/<content_id>/tags', methods=['POST'])
@jwt_required()
def associate_tags_with_content(content_id):
    data = request.get_json()
    tag_ids = data.get('tag_ids', [])

    content = contents.find_one({'_id': content_id})
    if not content:
        return jsonify({"error": "Content not found"}), 404
    
    tags_list = tags.find({'_id': {'$in': tag_ids}})
    contents.update_one({'_id': content_id}, {'$set': {'tags': [tag['_id'] for tag in tags_list]}})
    return jsonify({"message": "Tags associated with content successfully"}), 200

# User model
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if users.find_one({'username': username}):
        return jsonify({"error": "Username already exists"}), 400

    user = {
        'username': username,
        'password_hash': generate_password_hash(password),
        'email': email
    }
    users.insert_one(user)
    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 201

@app.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    data = request.get_json()
    preferences = data.get('preferences')

    user = users.find_one({'username': current_user})
    if user:
        users.update_one({'username': current_user}, {'$set': {'preferences': preferences}})
        return jsonify({"message": "Profile updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = users.find_one({'username': current_user})
    if user:
        return jsonify({"username": user['username'], "email": user['email'], "preferences": user.get('preferences', '')}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.find_one({'username': username})
    if user and check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/log_activity', methods=['POST'])
@jwt_required()
def log_activity():
    current_user = get_jwt_identity()
    data = request.get_json()
    action = data.get('action')

    log = {
        'username': current_user,
        'action': action,
        'timestamp': datetime.now()
    }
    # Insert the log into the MongoDB collection
    activity_logs.insert_one(log)
    return jsonify({"message": "Activity logged successfully"}), 201


@app.route('/get_logs', methods=['GET'])
@jwt_required()
def get_logs():
    current_user = get_jwt_identity()
    logs = activity_logs.find({'username': current_user})
    
    # Format logs for output
    formatted_logs = [
        {
            'action': log['action'],
            'timestamp': log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        }
        for log in logs
    ]
    
    return jsonify({"logs": formatted_logs}), 200




















@app.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    current_user = get_jwt_identity()
    logs = activity_logs.find({'username': current_user})
    analytics = [{"action": log['action'], "timestamp": log['timestamp']} for log in logs]
    return jsonify({"analytics": analytics}), 200

# Route to update or add user preferences
@app.route('/preferences', methods=['POST'])
def save_preferences():
    data = request.json
    user_id = data.get('user_id')
    preferences = data.get('preferences')

    if not user_id or not preferences:
        return jsonify({'error': 'Missing user_id or preferences'}), 400

    user_preferences = {
        "user_id": ObjectId(user_id),
        "preferences": preferences
    }

    # Upsert operation to update or create user preferences
    result = mongo.db.user_preferences.update_one(
        {"user_id": ObjectId(user_id)},
        {"$set": user_preferences},
        upsert=True
    )

    return jsonify({"message": "Preferences updated successfully"}), 200

@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    user_preferences = db.user_preferences.find_one({"user_id": ObjectId(user_id)})
    print("User Preferences: ", user_preferences)  # Debugging
    
    if not user_preferences:
        return jsonify({"error": "User not found"}), 404
    
    preferences = user_preferences.get("preferences", [])
    requested_tags = request.args.getlist('tags')  # New addition: Get tags from query parameters

    query = {"category": {"$in": preferences}}

    if tags: # Add tags to the query if provided
        query["tags"] = {"$in": tags}

    recommendations = list(db.content.find(query))

    # Ensure ObjectIds are serialized
    for rec in recommendations:
        rec["_id"] = str(rec["_id"])

    print("Preferences: ", preferences)  # Debugging
    
    recommendations = list(db.content.find({"category": {"$in": preferences}}))
    print("Recommendations: ", recommendations)  # Debugging
    
    for recommendation in recommendations:
        recommendation['_id'] = str(recommendation['_id'])
    
    return jsonify(recommendations), 200


@app.route('/search', methods=['GET'])
def search_content():
    category = request.args.get('category')
    tags = request.args.getlist('tags')

    query = {}
    if category:
        query['category'] = {'$regex': f'^{category}$', '$options': 'i'}  # Case-insensitive search for category
    if tags:
        query['tags'] = {'$in': tags}

    results = contents.find(query)
    search_results = []

    for result in results:
        search_results.append({
            "id": str(result["_id"]),
            "title": result.get("title"),
            "category": result.get("category"),
            "tags": result.get("tags", [])
        })

    return jsonify(search_results), 200




@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'GET method works!'})

if __name__ == '__main__':
    app.run(debug=True)
