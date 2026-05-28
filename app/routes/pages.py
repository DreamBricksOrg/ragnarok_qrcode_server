from pathlib import Path

from flask import Blueprint, abort, current_app, render_template, send_from_directory

from app.utils.validators import is_uuid


pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/css/<path:filename>", endpoint="css")
def css(filename: str):
    css_dir = Path(current_app.root_path) / "templates" / "css"
    return send_from_directory(css_dir, filename)


@pages_bp.get("/images/<path:filename>", endpoint="images")
def images(filename: str):
    images_dir = Path(current_app.root_path) / "templates" / "images"
    return send_from_directory(images_dir, filename)


@pages_bp.get("/fonts/<path:filename>", endpoint="fonts")
def fonts(filename: str):
    fonts_dir = Path(current_app.root_path) / "templates" / "fonts"
    return send_from_directory(fonts_dir, filename)


@pages_bp.get("")
@pages_bp.get("/")
def generic_coupon_page():
    return render_template("generic_coupon.html")


@pages_bp.get("/demo")
def demo_page():
    if current_app.config["ENV_NAME"] != "development":
        abort(404)

    return render_template(
        "demo.html",
        api_key=current_app.config["API_KEY"],
        base_url=current_app.config["BASE_URL"].rstrip("/"),
    )


@pages_bp.get("/<coupon_id>")
def coupon_page(coupon_id: str):
    if not is_uuid(coupon_id):
        return "invalid coupon id", 400

    return render_template("coupon.html", coupon_id=coupon_id)
