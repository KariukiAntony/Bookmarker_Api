from flask import Flask
from src.auth import auth
from src.Bookmarks import Bookmarks
from src.database import db
import os
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"),
                                SQLALCHEMY_DATABASE_URI =os.environ.get("S_D_U"),
                                SQLALCHEMY_TRACK_MODIFICATION = False,
                                JWT_SECRET_KEY = os.environ.get("jwt_key")
                                )
    else:
        app.config.from_mapping(test_config)

    
    db.init_app(app)
    JWTManager(app)
    # with app.app_context():
    #         db.create_all()
    #         print("bookmarks.db created successfully")
    app.register_blueprint(auth)
    app.register_blueprint(Bookmarks)
    
    return app  