from flask import Flask

from app.routes.coupons import api_bp
from app.routes.docs import docs_bp
from app.routes.health import health_bp
from app.routes.pages import pages_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(pages_bp, url_prefix="/pages")
    app.register_blueprint(docs_bp, url_prefix="/docs")
