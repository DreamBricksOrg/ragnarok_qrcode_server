from flask import Blueprint, current_app, jsonify, request

from app.auth import require_api_key
from app.repositories.coupon_repository import CouponRepository
from app.services.coupon_service import CouponService
from app.services.logcenter_client import LogCenterClient
from app.utils.validators import is_uuid


api_bp = Blueprint("api", __name__)


def get_coupon_service() -> CouponService:
    return CouponService(CouponRepository())


def get_logger() -> LogCenterClient:
    return LogCenterClient.from_app(current_app._get_current_object())


def _collect_request_data() -> dict:
    return {
        "ip": request.remote_addr,
        "x_forwarded_for": request.headers.get("X-Forwarded-For"),
        "user_agent": request.headers.get("User-Agent"),
        "referer": request.headers.get("Referer"),
        "origin": request.headers.get("Origin"),
        "accept_language": request.headers.get("Accept-Language"),
        "accept": request.headers.get("Accept"),
        "host": request.headers.get("Host"),
        "method": request.method,
        "path": request.path,
        "scheme": request.scheme,
        "content_type": request.content_type or None,
        "is_secure": request.is_secure,
    }


@api_bp.get("/genragcode")
@require_api_key
def generate_code_url():
    base_url = current_app.config["BASE_URL"]
    response = get_coupon_service().generate_url(base_url)
    success = response.get("url") is not None
    status_code = 200 if success else 404

    logger = get_logger()
    if success:
        logger.log(
            level="INFO",
            status="success",
            message="URL de cupom gerada",
            tags=["coupon", "generate", "success", "server"],
        )
    else:
        logger.log(
            level="WARN",
            status="failed",
            message="Tentativa de gerar URL sem cupons disponíveis",
            tags=["coupon", "generate", "failed", "server"],
        )

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

    repo = CouponRepository()
    service = CouponService(repo)
    response = service.redeem(coupon_id)
    success = response["status"] == "success"
    status_code = 200 if success else 409

    # resolve code for logging: success already has it; for failures fetch from DB
    code = response.get("code")
    if code is None:
        coupon = repo.find_by_id(coupon_id)
        code = coupon["code"] if coupon else None

    data = _collect_request_data()
    data["code"] = code
    if not success:
        data["failure_reason"] = response.get("message")

    logger = get_logger()
    if success:
        logger.log(
            level="INFO",
            status="success",
            message=f"Cupom resgatado: {code}",
            data=data,
            tags=["coupon", "redeem", "success", "server"],
        )
    else:
        logger.log(
            level="WARN",
            status="failed",
            message=f"Falha ao resgatar cupom: {code or coupon_id} — codigo ja resgatado",
            data=data,
            tags=["coupon", "redeem", "failed", "server"],
        )

    return jsonify(response), status_code
