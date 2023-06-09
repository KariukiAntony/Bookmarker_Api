from flask import Flask, jsonify, redirect
from src.auth import auth
from src.Bookmarks import Bookmarks
from src.database import db, Bookmark
import os
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from src.constants.HTTP_STATUS_CODES import *
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"),
                                SQLALCHEMY_DATABASE_URI =os.environ.get("S_D_U"),
                                SQLALCHEMY_TRACK_MODIFICATION = False,
                                JWT_SECRET_KEY = os.environ.get("jwt_key"),
                                SWAGGER={"title": "Bookmarks API", 
                                         "uiversion": 3}
                                )
    else:
        app.config.from_mapping(test_config)

    Swagger(app, config=swagger_config, template=template)
    db.init_app(app)
    JWTManager(app)
    # with app.app_context():
    #         db.create_all()
    #         print("bookmarks.db created successfully")
    app.register_blueprint(auth)
    app.register_blueprint(Bookmarks)

    @app.get("/<short_url>")
    @swag_from("./docs/short_url.yaml")
    def redirect_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        if bookmark:
            print(bookmark.short_url)
            bookmark.visits = bookmark.visits +1
            db.session.commit()
            return redirect(bookmark.url)
        
    @app.get("/stats")
    @jwt_required()
    @swag_from("./docs/bookmarks/stats.yaml")
    def bookmark_stats():
        user_id = get_jwt_identity()
        items = Bookmark.query.filter_by(user_id=user_id).all()
        data = []
        for item in items:
            stats = {"id": item.id,
                     "url": item.url,
                     "short_url": item.short_url,
                     "visits": item.visits}
            data.append(stats)
        return jsonify({"data": data}), HTTP_200_OK
    
        
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error":"The page you are loking for cannot be found"}), HTTP_404_NOT_FOUND
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong, we are working on it."}), HTTP_500_INTERNAL_SERVER_ERROR

    
    return app  