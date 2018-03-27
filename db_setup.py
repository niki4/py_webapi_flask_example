from model.db import Base, engine, Session, Product, Category, Feature

products_info = [
    {
        'title': 'Iphone X',
        'price_rub': 100500,
        'product_image': 'images/iphone_x.jpg',
        'in_store': True,
        'category': 2,
    },
    {
        'title': 'Macbook Air 2015',
        'price_rub': 500100,
        'product_image': 'images/macbook_2015.jpg',
        'in_store': True,
        'category': 1,
    },
    {
        'title': 'Macbook Air 2017',
        'price_rub': 777000,
        'product_image': 'images/macbook_2017.jpg',
        'in_store': False,
        'category': 1,
    },
]

product_categories = [
    {'category': 'Laptops'},
    {'category': 'Smartphones'},
    {'category': 'Tablets'},
]

category_features = [
    {'feature': 'bluetooth', 'category': 1},
    {'feature': 'wifi', 'category': 1},
    {'feature': 'gps', 'category': 2},
]


def create_demo_products():
    session = Session()
    for product_info in products_info:
        product = Product()
        product.title = product_info['title']
        product.price_rub = product_info['price_rub']
        product.product_image = product_info['product_image']
        product.in_store = product_info['in_store']
        product.category_id = product_info['category']
        session.add(product)
    for category_info in product_categories:
        category = Category()
        category.category_name = category_info['category']
        session.add(category)
    for feature_info in category_features:
        feature = Feature()
        feature.name = feature_info['feature']
        feature.category_id = feature_info['category']
        session.add(feature)
    session.commit()


def create_all_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all_tables()
    create_demo_products()
