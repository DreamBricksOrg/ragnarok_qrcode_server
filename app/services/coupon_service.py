import csv
from io import TextIOWrapper
from uuid import uuid4

from app.repositories.coupon_repository import CouponRepository
from app.utils.validators import is_uuid


class CouponService:
    def __init__(self, repository: CouponRepository) -> None:
        self.repository = repository

    def generate_url(self, base_url: str) -> dict:
        coupon = self.repository.find_valid()

        if coupon is None:
            return {"status": "failed", "message": "no valid codes available"}

        return {"url": f"{base_url.rstrip('/')}/pages/{coupon['_id']}"}

    def import_csv(self, file_storage) -> dict:
        reader = csv.DictReader(TextIOWrapper(file_storage.stream, encoding="utf-8-sig"))

        if not reader.fieldnames:
            raise ValueError("csv file is empty")

        required_columns = {"code", "valid"}
        missing_columns = required_columns - set(reader.fieldnames)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"missing csv columns: {missing}")

        coupons = [self._build_coupon(row) for row in reader]
        inserted = self.repository.create_many(coupons)

        return {"status": "success", "inserted": inserted}

    def redeem(self, coupon_id: str) -> dict:
        if not is_uuid(coupon_id):
            return {"status": "failed", "message": "invalid coupon id"}

        redeemed = self.repository.redeem(coupon_id)

        if redeemed:
            return {"status": "success", "code": redeemed["code"]}

        coupon = self.repository.find_by_id(coupon_id)

        if coupon:
            return {"status": "failed", "message": "already used"}

        return {"status": "failed", "message": "code not found"}

    def _build_coupon(self, row: dict) -> dict:
        coupon_id = (row.get("id") or "").strip() or str(uuid4())
        code = row.get("code", "").strip()
        valid = row.get("valid", "").strip().lower()

        if not code:
            raise ValueError("code is required")

        if not is_uuid(coupon_id):
            raise ValueError("id must be a valid uuid")

        if valid not in {"valid", "notvalid"}:
            raise ValueError("valid must be valid or notvalid")

        return {
            "_id": coupon_id,
            "code": code,
            "valid": valid,
        }
