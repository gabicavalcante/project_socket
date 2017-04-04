from pymongo import MongoClient

from dbsettings import MONGO

client = MongoClient(
    'mongodb://{}:{}@{}/{}'.format(MONGO['username'], MONGO['password'], MONGO['host'], MONGO['database']))

db = client.socket_database
users_collection = db.users
tokens_collection = db.tokens


def create_users():
    user01 = {
        'username': 'username01',
        'password': '12345',
        'email': 'gabicavalcantesilva@gmail.com'
    }

    user02 = {
        'username': 'username02',
        'password': '12345',
        'email': 'raivitor@gmail.com'
    }

    user03 = {
        'username': 'username03',
        'password': '12345',
        'email': 'tres.daniel.s@gmail.com'
    }

    id01 = users_collection.insert_one(user01).inserted_id
    id02 = users_collection.insert_one(user02).inserted_id
    id03 = users_collection.insert_one(user03).inserted_id

    print 'id01: {} | id02: {} | id03: {}'.format(id01, id02, id03)
