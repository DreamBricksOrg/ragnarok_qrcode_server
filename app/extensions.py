from pymongo import MongoClient
from pymongo.database import Database


class Mongo:
    def __init__(self) -> None:
        self.client: MongoClient | None = None
        self.db: Database | None = None

    def init_app(self, app) -> None:
        self.client = MongoClient(app.config["MONGO_URI"])
        self.db = self.client.get_default_database()


mongo = Mongo()
