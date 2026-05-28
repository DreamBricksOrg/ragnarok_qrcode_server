from flask import Flask

from app.config import get_config
from app.errors import register_error_handlers
from app.extensions import mongo
from app.routes import register_routes


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    mongo.init_app(app)
    register_error_handlers(app)
    register_routes(app)

    return app
