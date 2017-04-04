import logging

import tokenlib
from datetime import datetime

import sys

sys.path.append('../')
from db import tokens_collection


def generate_token(user_id):
    if tokens_collection.find({"user_id": user_id}).count() == 0:
        logging.info('creating token...')
        token = tokenlib.make_token({"user_id": user_id}, secret="I_LIKE_UNICORNS")
        return token
    else:
        logging.info("token exist...")
        data_token = str(tokens_collection.find_one({"user_id": user_id}))
        token = data_token['key']
        if validate_token(token):
            return token
        else:
            token = tokenlib.make_token({"user_id": user_id}, secret="I_LIKE_UNICORNS")
            return token


def save_token(token):
    id = None
    data = tokenlib.parse_token(token, secret="I_LIKE_UNICORNS")
    print data
    data_token = {
        "key": token,
        "expires": data['expires'],
        "user_id": data['user_id'],
        "salt": data['salt']
    }
    if tokens_collection.find({"user_id": data['user_id']}).count() == 0:
        id = tokens_collection.insert_one(data_token).inserted_id
    return id


def validate_token(token):
    try:
        tokenlib.parse_token(token, secret="I_LIKE_UNICORNS", now=datetime.now())
    except ValueError:
        return False
    return True
