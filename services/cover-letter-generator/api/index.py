from flask import request, current_app as app
from .helpers.helper import (
    make_response_json,
)

def main():
    """
    main function
    """
    try:
        return make_response_json({"message": "Hellooooo", "status": 200}, 200)
    except Exception as e:
        return make_response_json({"message": str(e), "status": 500}, 500)