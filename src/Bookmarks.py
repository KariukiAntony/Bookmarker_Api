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
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("pages", 5, type=int)
        bookmarks = Bookmark.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page,error_out=False)
        serialized = []
        for bookmark in bookmarks.items:
            serialized.append({"id":bookmark.id,
                               "body": bookmark.body,
                                "url": bookmark.url, 
                                "short_url": bookmark.short_url,
                                "visits": bookmark.visits,
                                "created_at": bookmark.created_at, 
                                "updated_at": bookmark.updated_at})
        meta = {"page": bookmarks.page,
                "pages": bookmarks.pages,
                "items_per_page": bookmarks.per_page,
                "prev_pages":bookmarks.prev_num,
                "next_pages": bookmarks.next_num,
                "total_count": bookmarks.total,
                "has_prev": bookmarks.has_prev,
                "has_next": bookmarks.has_next
                }
        return jsonify(serialized, {"meta": meta}), HTTP_200_OK
    
@Bookmarks.route("/<int:id>")
@jwt_required()
def get_bookmark(id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=user_id, id=id).first()
    if not bookmark:
        return jsonify({"error": "bookmark with this id does not exist"}), HTTP_404_NOT_FOUND
    else:
        print(bookmark.created_at)
        return jsonify({"id":bookmark.id,
                            "body": bookmark.body,
                            "url": bookmark.url, 
                            "short_url": bookmark.short_url,
                            "visits": bookmark.visits,
                            "created_at": bookmark.created_at, 
                            "updated_at": bookmark.updated_at})
    

@Bookmarks.put("/<int:id>")
@Bookmarks.patch("/<int:id>")
@jwt_required()
def edit_bookmarks(id):
    user_id = get_jwt_identity()
    body = request.json.get("body")
    url = request.json.get("url")
    bookmark = Bookmark.query.filter_by(user_id=user_id, id=id).first()
    if not bookmark:
        return jsonify({"error": "bookmark does not exist"}), HTTP_404_NOT_FOUND
    if not validators.url(url):
        return jsonify({"error": "Invalid url"}), HTTP_400_BAD_REQUEST
    else:
        bookmark.body = body
        bookmark.url = url
        db.session.commit()

        return jsonify({"id": id,
                        "url":bookmark.url,
                        "body": bookmark.body,
                        "short_url": bookmark.short_url,
                        "visits": bookmark.visits,
                        "created_at": bookmark.created_at,
                        "updated_at": bookmark.updated_at}), HTTP_200_OK

    