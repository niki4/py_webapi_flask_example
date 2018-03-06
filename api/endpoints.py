from flask import request, jsonify, render_template

from api import app
from db import PRODUCTS
from server import validate_product


@app.route('/api/v1/products/', methods=['GET', 'POST'])
def products_handle():
    if request.method == 'GET':
        search_query = request.args.get('q')
        products_to_show = PRODUCTS
        if search_query:
            products_to_show = [p for p in PRODUCTS if search_query.lower() in p['title'].lower()]

        is_only_in_store = 'only_in_store' in request.args
        if is_only_in_store:
            products_to_show = [p for p in PRODUCTS if p['in_store']]

        raw_from = request.args.get('from')
        raw_to = request.args.get('to')
        if (raw_from and raw_to) and (raw_from.isdigit() and raw_to.isdigit()):
            products_to_show = products_to_show[int(raw_from):int(raw_to)]

        raw_fields = request.args.get('fields')
        if raw_fields:
            iter_fields = raw_fields.split(',')
            products_to_show = [{k: v for (k, v) in p.items() if k in iter_fields} for p in products_to_show]
        return jsonify(products_to_show)
    elif request.method == 'POST':
        errors, request_data = validate_product(request.data.decode('utf-8'))
        if not errors:
            PRODUCTS.append(request_data)
            return jsonify('ok')
        else:
            response = jsonify(errors)
            response.status_code = 400
            return response


@app.route('/hello/', methods=['GET'])
@app.route('/hello/<name>')
def hello(name=None):
    print(request.method)
    return render_template('hello.html', name=name)
