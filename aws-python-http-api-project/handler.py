import json
import logging

import boto3
import jwt
from services.dynamodb import Users

logging.getLogger().setLevel(logging.INFO)

def login(event, context):
    
    body = json.loads(event["body"])

    name = body.get("name")
    password = body.get("password")

    logging.info(f"{name=}")
    logging.info(f"{password=}")
    logging.info(f"{body=}")

    if not name or not password:
        return {
            'statusCode': 403,
            "body": json.dumps("Unauthorized: Name or password was not passed")
        }

    
    table = boto3.resource('dynamodb').Table("usersTable")
    users = Users(table)

    found_password = users.get_user(username=name).get("password")

    logging.info(f"{found_password=}")

    if found_password != password:
        return {"statusCode": 403, "body": json.dumps({"reason": "incorrect password"})}
    
    payload = {
        "username": name,
        "password": password
    }

    my_secret = 'my_super_secret'

    token = jwt.encode(payload=payload, key=my_secret)
    
    body = {
        "token": token
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def hello(event,context):
  return {
    'body': f'Hello there',
    'headers': {
      'Content-Type': 'text/plain'
    },
    'statusCode': 200
  }
