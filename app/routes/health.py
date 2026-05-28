from flask import Blueprint, jsonify

from app.extensions import mongo


health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def health_check():
    mongo.client.admin.command("ping")

    return jsonify(
        {
            "status": "alive"
        }
    )
