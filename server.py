from api.views import register_endpoints
from api import app
from model.db import Product, Category, Feature

BASE_URL = '/api/v1/'

register_endpoints(app, Product,  base_url=BASE_URL, _search_field_name='title')
# register_endpoints(app, Category, base_url=BASE_URL)
# register_endpoints(app, Feature,  base_url=BASE_URL)

if __name__ == '__main__':
    app.run(port=5000)
