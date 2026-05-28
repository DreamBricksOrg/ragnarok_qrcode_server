from flask import Blueprint, current_app, jsonify, request

from app.auth import require_api_key
from app.repositories.coupon_repository import CouponRepository
from app.services.coupon_service import CouponService
from app.utils.validators import is_uuid


api_bp = Blueprint("api", __name__)


def get_coupon_service() -> CouponService:
    return CouponService(CouponRepository())


@api_bp.get("/genragcode")
@require_api_key
def generate_code_url():
    base_url = current_app.config["BASE_URL"]
    response = get_coupon_service().generate_url(base_url)
    status_code = 200 if response.get("url") else 404

    return jsonify(response), status_code


@api_bp.post("/import/codes")
@require_api_key
def import_codes():
    csv_file = request.files.get("csv")

    if csv_file is None:
        raise ValueError("csv file is required")

    response = get_coupon_service().import_csv(csv_file)

    return jsonify(response), 201


@api_bp.get("/<coupon_id>")
def redeem_code(coupon_id: str):
    if not is_uuid(coupon_id):
        return jsonify({"status": "failed", "message": "invalid coupon id"}), 400

    response = get_coupon_service().redeem(coupon_id)
    status_code = 200 if response["status"] == "success" else 409

    return jsonify(response), status_code
