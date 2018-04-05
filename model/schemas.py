from marshmallow import Schema, fields, ValidationError


class ProductSchema(Schema):
    title = fields.Str(required=True)
    price_rub = fields.Int(required=True)
    product_image = fields.Str(required=False)
    in_store = fields.Bool(required=False)


def validate_product_schema(request_data):
    return ProductSchema().validate(request_data)
