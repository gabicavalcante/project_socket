from pymongo import MongoClient
from pymongo import ASCENDING
import datetime

from settings import LOG_SETTINGS

mongo = LOG_SETTINGS['handlers']['mongodb']

client = MongoClient('mongodb://{}:{}@{}/{}'.format(mongo['username'], mongo['password'], mongo['host'], mongo['database_name']))

db = client.MONGO['username']
log_collection = db.log
log_collection.ensure_index([("timestamp", ASCENDING)])

print log_collection.find_one()