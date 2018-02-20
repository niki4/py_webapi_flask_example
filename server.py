import json

from marshmallow import Schema, fields

import api.endpoints


class ProductSchema(Schema):
    title = fields.Str(required=True)
    price_rub = fields.Int(required=True)
    product_image = fields.Str(required=False)
    in_store = fields.Bool(required=False)


def validate_product(raw_data):
    request_data = json.loads(raw_data)
    errors = ProductSchema().validate(request_data)
    return errors, request_data


if __name__ == '__main__':
    api.app.run(port=5000)
