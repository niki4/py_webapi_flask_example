import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import scoped_session, relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.TestingConfig.DB_URI, echo=True)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class AbstractModel:
    def to_dict(self, fields=None):
        result_info = {}
        for column in self.__class__.__table__.columns:
            if fields and column.name not in fields:
                continue
            result_info[column.name] = getattr(self, column.name, None)
        return result_info


class Product(Base, AbstractModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price_rub = Column(Integer)
    product_image = Column(String)
    in_store = Column(Boolean)
    category_id = Column(Integer, ForeignKey('categories.id'))

    @classmethod
    def from_dict(cls, product_info):
        product = cls()
        product.price_rub = product_info.get('price_rub')
        product.product_image = product_info.get('product_image')
        product.title = product_info.get('title')
        product.in_store = product_info.get('in_store')
        product.category_id = product_info.get('category_id')
        return product


class Category(Base, AbstractModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    products = relationship('Product')
    features = relationship('Feature')


class Feature(Base, AbstractModel):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
