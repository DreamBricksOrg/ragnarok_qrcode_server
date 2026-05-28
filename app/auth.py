from functools import wraps

from flask import current_app, jsonify, request


def require_api_key(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        api_key = (
            request.headers.get("api-key")
            or request.headers.get("x-api-key")
            or request.headers.get("api_key")
        )

        if api_key != current_app.config["API_KEY"]:
            return jsonify({"status": "failed", "message": "invalid api_key"}), 401

        return handler(*args, **kwargs)

    return wrapper
