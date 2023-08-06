from mongoengine import connect
from nleaser_config import MONGO_HOST, MONGO_PORT, MONGO_DB


def connect_db():
    connect(
        db=MONGO_DB,
        host=MONGO_HOST,
        port=MONGO_PORT
    )
