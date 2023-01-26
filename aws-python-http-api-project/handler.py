import json

import jwt


def login(event, context):
    
    body = json.loads(event["body"])

    name = body.get("name")
    password = body.get("password")

    print(f"{name=}")
    print(f"{password=}")
    print(f"{body=}")

    if not name or not password:
        return {
            'statusCode': 403,
            "body": json.dumps("Unauthorized: Name or password was not passed")
        }
    
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
