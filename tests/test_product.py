import os
import json
import pytest

from config import TestingConfig
from db_setup import create_all_tables, create_demo_products, products_info
from api import app
from api.views import register_endpoints
from model import db

API_URL = TestingConfig.BASE_URL

test_products = [
    {
        'title': 'Nexus X',
        'price_rub': 99999,
        'product_image': 'images/nexus_x.jpg',
        'in_store': False,
        'category_id': 1,
    },
    {
        'title': 123,
        'price_rub': 'i am string',
    },
    {
        'price_rub': 1,
    },
]
test_categories = [
    {'category': 'SSD'},
]
test_features = [
    {'feature': 'NFC', 'category': 2},
]


def setup_module(module):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), os.path.pardir, 'db.sqlite')):
        create_all_tables()
        create_demo_products()

    app.config.from_object('config.TestingConfig')
    register_endpoints(app, db.Product, base_url=TestingConfig.BASE_URL, _search_field_name='title')


client = app.test_client()


def get_product_list(endpoint='product/'):
    response = client.get('{}{}'.format(API_URL, endpoint), follow_redirects=True)
    result = json.loads(response.get_data(as_text=True))
    return response, result


def test_get_product_list():
    response, result = get_product_list()
    assert response.status_code == 200
    assert len(result)
    for product in result:
        assert 'title' in product


def test_product_list_endpoint_without_trailing_slash():
    response, result = get_product_list(endpoint='product')
    assert response.status_code == 200
    assert len(result)
    for product in result:
        assert 'title' in product


def test_get_product_list_by_url_param_q():
    query = products_info[0]['title'].split()[0].lower()
    response = client.get('{}product/?q={}'.format(API_URL, query))
    assert response.status_code == 200

    result = json.loads(response.get_data(as_text=True))
    for product in result:
        assert query in product['title'].lower()


@pytest.mark.parametrize('from_, to_', [(0, 2), (1, 3)])
def test_get_product_list_by_url_params_from_to(from_, to_):
    response = client.get('{}product/?from={}&to={}'.format(API_URL, from_, to_))
    assert response.status_code == 200

    result = json.loads(response.get_data(as_text=True))
    assert len(result) == to_-from_


def test_get_product_by_url_path_id():
    response = client.get('{}product/2'.format(API_URL))
    assert response.status_code == 200

    result = json.loads(response.get_data(as_text=True))
    assert result['id'] == 2


def test_create_product_valid_data():
    response = client.post('{}product/'.format(API_URL), data=json.dumps(test_products[0]))
    assert response.status_code == 200

    product_list_titles = [product['title'] for product in get_product_list()[1]]
    assert test_products[0]['title'] in product_list_titles


def test_create_product_invalid_data():
    response = client.post('{}product/'.format(API_URL), data=json.dumps(test_products[1]))
    assert response.status_code == 400

    result = json.loads(response.get_data(as_text=True))
    assert 'Not a valid integer' in result['price_rub'][0]

    product_list_titles = [product['title'] for product in get_product_list()[1]]
    assert test_products[1]['title'] not in product_list_titles


def test_create_product_missed_required_data():
    response = client.post('{}product/'.format(API_URL), data=json.dumps(test_products[2]))
    assert response.status_code == 400

    result = json.loads(response.get_data(as_text=True))
    assert 'Missing data' in result['title'][0]

    product_list_titles = [product['title'] for product in get_product_list()[1]]
    assert test_products[1]['title'] not in product_list_titles
