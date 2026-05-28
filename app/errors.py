from flask import Flask, jsonify


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):
        return jsonify({"error": str(error)}), 400
