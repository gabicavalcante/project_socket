import logging

import tokenlib
from datetime import datetime

import sys

sys.path.append('../')
from db import tokens_collection


def generate_token(data):
    if tokens_collection.find({"user_id": data}).count() == 0:
        logging.info('creating token...')
        token = tokenlib.make_token({"user_id": data}, secret="I_LIKE_UNICORNS")
        return token
    else:
        logging.info("token exist...")
        token = tokens_collection.find_one({"user_id": data})
        return token['key']


def save_token(token):
    data = tokenlib.parse_token(token, secret="I_LIKE_UNICORNS")
    data_token = {
        "key": token,
        "expires": data['expires'],
        "user_id": data['user_id'],
        # "issued_at": str(datetime.now())
    }
    if tokens_collection.find({"user_id": data['user_id']}).count() == 0:
        tokens_collection.insert_one(data_token).inserted_id


def validate_token(token):
    try:
        tokenlib.parse_token(token, secret="I_LIKE_UNICORNS", now=datetime.now())
        return True
    except ValueError:
        return False
