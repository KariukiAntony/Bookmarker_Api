from flask import Blueprint, jsonify, request
from src.constants.HTTP_STATUS_CODES import *
from flask_jwt_extended import  jwt_required, get_jwt_identity
from src.database import db, Bookmark
import validators

Bookmarks = Blueprint("Bookmarks", __name__, url_prefix="/api/v1/Bookmarks")

@Bookmarks.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_bookmarks():
    user_id = get_jwt_identity()
    if request.method == "POST":
        body = request.json.get("body")
        url = request.json.get("url")
        if not url:
            return jsonify({"error": "url required"}), HTTP_400_BAD_REQUEST
        
        if not validators.url(url):
            return jsonify({"error": "Invalid url"}), HTTP_400_BAD_REQUEST
        
        existing_url = Bookmark.query.filter_by(url=url).first()
        if existing_url:
            return jsonify({"error": "url already exist"}), HTTP_409_CONFLICT
        
        bookmark = Bookmark(body=body, url=url, user_id=user_id)
        print("yooh")
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({"id": bookmark.id,
                        "body": bookmark.body,  
                        "url": bookmark.url,
                        "short_url": bookmark.short_url,
                        "visits": bookmark.visits,
                        "created_at": bookmark.created_at, 
                        "updated_at": bookmark.updated_at}), HTTP_201_CREATED
    
    elif request.method == "GET":
        bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
        serialized = []
        for bookmark in bookmarks:
            serialized.append({"id":bookmark.id,
                               "body": bookmark.body,
                                "url": bookmark.url, 
                                "short_url": bookmark.short_url,
                                "visits": bookmark.visits,
                                "created_at": bookmark.created_at, 
                                "updated_at": bookmark.updated_at})
        return jsonify(serialized), HTTP_200_OK



    