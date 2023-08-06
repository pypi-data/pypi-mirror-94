import json
from LambdaPage import LambdaPage
import murd_ddb as murd


def update_handler(event):
    body = json.loads(event['body'])
    murdis = json.loads(body)
    murd.update(murdis)
    return 200


def read_handler(event):
    body = json.loads(event['body'])
    region = body['REGION']
    sort = body['SORT'] if 'SORT' in body else None
    max_sort = body['MAX_SORT'] if 'MAX_SORT' in body else None
    min_sort = body['MIN_SORT'] if 'MIN_SORT' in body else None
    limit = body['LIMIT'] if 'LIMIT' in body else None

    read_kwargs = {
        "region": region,
        "sort": sort,
        "max_sort": max_sort,
        "min_sort": min_sort,
        "limit": limit
    }
    read = murd.read(**read_kwargs)

    return 200, json.dumps(read)


def delete_handler(event):
    body = json.loads(event['body'])
    murdis = body['murdis']
    stubborn_murdis = murd.delete(murdis)
    return 200, json.dumps(stubborn_murdis)


def create_lambda_page():
    page = LambdaPage()
    page.add_endpoint("get", "/", read_handler, "application/json")
    page.add_endpoint("put", "/", update_handler, "application/json")
    page.add_endpoint("delete", "/", delete_handler, "application/json")
    return page


def lambda_handler(event, handler):
    page = create_lambda_page()
    print("Received Event:\n{}".format(event))
    return page.handle_request(event)
