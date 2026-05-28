from flask import Blueprint, render_template

from app.utils.validators import is_uuid


pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/<coupon_id>")
def coupon_page(coupon_id: str):
    if not is_uuid(coupon_id):
        return "invalid coupon id", 400

    return render_template("coupon.html", coupon_id=coupon_id)
