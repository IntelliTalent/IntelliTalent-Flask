from flask import (
    Flask, 
    jsonify,
)
from .index import (
    main,
)

def create_app():
    app = Flask(__name__)

    # called on app install on a store
    app.route("/", methods=["GET"])(main)