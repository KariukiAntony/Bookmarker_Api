from flask import Blueprint

Bookmarks = Blueprint("Bookmarks", __name__, url_prefix="/api/v1/Bookmarks")

@Bookmarks.get("/")
def get_all():
    return {"Bookmarks": []}



    