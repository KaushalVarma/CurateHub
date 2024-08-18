from flask import Blueprint, request, jsonify
from src.models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "email": user.email,
        "preferences": user.preferences
    })

@user_profile_bp.route('/profile/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    preferences = request.json.get('preferences')
    user.preferences = preferences
    db.session.commit()

    return jsonify({"message": "Preferences updated successfully"}), 200
