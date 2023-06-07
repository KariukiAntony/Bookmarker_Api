from flask import Blueprint, request, jsonify
from src.constants.HTTP_STATUS_CODES import *
from src.database import db, User
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post("/register")
@swag_from("./docs/auth/register.yaml")
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    existing_email = User.query.filter_by(email=email).first()
    existing_username = User.query.filter_by(username=username).first()
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST
    
    elif len(username) < 2:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST
    
    elif existing_username:
        return jsonify({"error": "Username is already taken"}), HTTP_409_CONFLICT
    
    elif not username.isalnum() or " " in username:
        return jsonify({"error": "Username should not contain spaces and special character"}), HTTP_400_BAD_REQUEST
    
    elif not (validators.email(email)) or existing_email:
        return jsonify({"error": "Invalid email"}), HTTP_409_CONFLICT
    
    elif len(password) < 6:
        return jsonify({"error": "password must be atleast 6 characters"}), HTTP_400_BAD_REQUEST
    else:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f" new user '{username}' created successfully")
        return jsonify({"message": "User created",
                        "user": {"username": username, "email": email, "password": password}}), HTTP_200_OK
    
@auth.post("/login")
@swag_from("./docs/auth/login.yaml")
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    if not email or not password:
        return jsonify({"error" : "All fields are required"}), HTTP_400_BAD_REQUEST
    else:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                refresh_token = create_refresh_token(identity=user.id)
                access_token = create_access_token(identity=user.id)
                return jsonify({"User": {"username": user.username, "email": user.email, "refresh_token": refresh_token, "access_token": access_token}}), HTTP_200_OK
            else:
                return jsonify({"error": "invalid password"}), HTTP_401_UNAUTHORIZED
        else:
            return jsonify({"error": "email does not exist"}), HTTP_404_NOT_FOUND
        

@auth.get("/me")
@jwt_required()
def refresh():
    user_id = get_jwt_identity()
    print(user_id)
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({"user": {"username": user.username,
                                 "email": user.email}}), HTTP_200_OK
    else:
        return jsonify({"error": "This user does not exist"}), HTTP_404_NOT_FOUND
    

@auth.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
    user_id = get_jwt_identity()
    access = create_access_token(identity=user_id)
    return jsonify({"access_token": access})