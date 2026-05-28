from pymongo import ReplaceOne, ReturnDocument

from app.extensions import mongo


class CouponRepository:
    collection_name = "coupons"

    @property
    def collection(self):
        return mongo.db[self.collection_name]

    def create_many(self, coupons: list[dict]) -> int:
        if not coupons:
            return 0

        operations = [
            ReplaceOne({"_id": coupon["_id"]}, coupon, upsert=True)
            for coupon in coupons
        ]
        result = self.collection.bulk_write(operations, ordered=False)

        return result.upserted_count + result.modified_count

    def find_valid(self) -> dict | None:
        return self.collection.find_one({"valid": "valid"}, {"_id": 1})

    def find_by_id(self, coupon_id: str) -> dict | None:
        return self.collection.find_one({"_id": coupon_id})

    def redeem(self, coupon_id: str) -> dict | None:
        return self.collection.find_one_and_update(
            {"_id": coupon_id, "valid": "valid"},
            {"$set": {"valid": "notvalid"}},
            return_document=ReturnDocument.AFTER,
        )
