import json

from sqlalchemy import Boolean

from flask import jsonify, request, abort, render_template, json
from flask.views import MethodView

from model.db import Session
from model.schemas import is_valid_product

from model.db import AbstractModel, Product, Category, Feature


class AbstractListView(MethodView):
    allow_boolean_filters = True
    model = None
    search_field_name = None

    def get(self):
        session = Session()
        products_from_model = session.query(self.model)
        products_to_show = self.apply_search_params(products_from_model)
        if self.allow_boolean_filters:
            products_to_show = self.apply_boolean_filters(products_to_show)
        products_to_show = self.apply_page_limits_params(products_to_show)
        products_list = self.convert_to_jsonable(products_to_show)
        return jsonify(products_list)

    def post(self):
        session = Session()
        request_data = json.loads(request.data.decode('utf-8'))
        if is_valid_product(request_data):
            product = self.model.from_dict(request_data)
            session.add(product)
            session.commit()
            return jsonify('ok')
        else:
            abort(400, jsonify('data error'))

    def apply_boolean_filters(self, products_to_show):
        for column_name in self.get_boolean_column_names_from_model():
            param = 'only_%s' % column_name    # e.g., 'only_in_store'
            if param in request.args:
                products_to_show = products_to_show.filter(
                    getattr(self.model, column_name)
                )
        return products_to_show

    def apply_search_params(self, products_to_show):
        search_query = request.args.get('q')
        if search_query:
            ilike_query = '%%%s%%' % search_query
            search_field = getattr(self.model, self.search_field_name)
            products_to_show = products_to_show.filter(
                search_field.ilike(ilike_query)
            )
        return products_to_show

    def apply_page_limits_params(self, products_to_show):
        raw_from = request.args.get('from')
        raw_to = request.args.get('to')
        if (raw_from and raw_to) and (raw_from.isdigit() and raw_from.isdigit()):
            products_to_show = products_to_show[int(raw_from):int(raw_to)]
        return products_to_show

    def convert_to_jsonable(self, products_to_show):
        raw_fields = request.args.get('fields')
        iter_fields = raw_fields.split(',') if raw_fields else None
        return [p.to_dict(iter_fields) for p in products_to_show]

    @classmethod
    def get_boolean_column_names_from_model(cls):
        column_names = []
        for column in cls.model.__table__.columns:
            if isinstance(column.type, Boolean):
                column_names.append(column.name)
        return column_names


class AbstractProductView(MethodView):
    model = None

    def get(self, product_id):
        session = Session()
        product_from_model = session.query(self.model).filter_by(id=product_id).first()
        if not product_from_model:
            abort(404)
        return jsonify(product_from_model.to_dict())


def register_endpoints(app, model_class, base_url, _search_field_name=None):
    class ApiListView(AbstractListView):
        model = model_class
        search_field_name = _search_field_name

    class RenderListView(AbstractListView):
        model = model_class
        search_field_name = _search_field_name

        def __init__(self, template_name):
            self.template_name = template_name
            self.products_list = self.get()

        def dispatch_request(self):
            products_list = json.loads(self.products_list.data)
            return render_template(self.template_name, products=products_list)

    class ApiProductView(AbstractProductView):
        model = model_class

    class RenderProductView(AbstractProductView):
        model = model_class

        def get(self, product_id):
            product_from_model = json.loads(super().get(product_id).data)

            session = Session()
            features = session.query(Feature.name).filter(
                Feature.category_id == product_from_model['category_id']).all()

            return render_template('product_details.html', product=product_from_model, features=features)

    view_name = model_class.__name__.lower()

    # api urls for apps and services
    app.add_url_rule('%s/%s/' % (base_url.rstrip('/'), view_name),
                     view_func=ApiListView.as_view('api_%s_list' % view_name))

    app.add_url_rule('%s/%s/<int:product_id>' % (base_url.rstrip('/'), view_name),
                     view_func=ApiProductView.as_view('api_%s_details' % view_name))

    # rendered urls for browsers
    app.add_url_rule('/%s/' % view_name,
                     view_func=RenderListView.as_view(
                         '%s_list' % view_name,
                         template_name='product_list.html'))

    app.add_url_rule('/%s/<int:product_id>' % view_name,
                     view_func=RenderProductView.as_view('%s_details' % view_name))
