from flask import Blueprint, abort, current_app, render_template

from app.utils.validators import is_uuid


pages_bp = Blueprint("pages", __name__)


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
