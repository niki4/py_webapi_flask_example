from marshmallow import Schema, fields, ValidationError


class ProductSchema(Schema):
    title = fields.Str(required=True)
    price_rub = fields.Int(required=True)
    product_image = fields.Str(required=False)
    in_store = fields.Bool(required=False)


def is_valid_product(request_data):
    errors = ProductSchema().validate(request_data)
    return True if not errors else False
