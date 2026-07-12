from pymongo import MongoClient

from src.core.config import settings


class Database:
    client: MongoClient = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            cls.client = MongoClient(settings.MONGO_URI)
            cls.db = cls.client[settings.MONGO_DB_NAME]
        return cls.db

    @classmethod
    def get_collection(cls, name: str):
        return cls.connect()[name]

    @classmethod
    def ping(cls) -> None:
        # called at startup, raises if MongoDB is not reachable
        cls.connect()
        cls.client.admin.command("ping")

    @classmethod
    def close(cls):
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.db = None
