from api.views import register_endpoints
from api import app
from model.db import Product

register_endpoints(app, Product, _search_field_name='title', base_url='/api/v1/')


if __name__ == '__main__':
    app.run(port=5000)
