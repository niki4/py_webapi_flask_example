[![Build Status](https://travis-ci.org/niki4/py_webapi_flask_example.svg?branch=master)](https://travis-ci.org/niki4/py_webapi_flask_example)

Simple example of the wsgi-compatible API web app using Flask framework.

# Setup
Once you've cloned the repo from GitHub, make sure you've created a virtual environment for experiments.
```
sudo pip3 install virtualenv
python3 -m virtualenv ./venv
source venv/bin/activate
```
Now you can install some dependencies (flask, marshmallow, etc.):
```
pip3 install -r requirements.txt
```
The project requires db to be created. Simply run following script, it will create db structure and some initial test data:
```
python db_setup.py
```
# Usage
Simply run the server:
```
python server.py
```
Now open browser and try the following API routes:
```
http://127.0.0.1:5000/api/v1/product/?q=iphone
http://127.0.0.1:5000/api/v1/product/?from=0&to=2
```
Note on the params stated after ? symbol in URL.

They are defined in views.py, whilst the db models are from db.py

To list all available products data set url endpoint without params:
```
http://127.0.0.1:5000/api/v1/product/
```
To view one desired product data just specify its id after endpoint:
```
http://127.0.0.1:5000/api/v1/product/1
```

## Rendering for browsers
Flask uses [Jinja2](http://jinja.pocoo.org/) templates engine under hood. That means you may see the data in a pretty human-readable view with your browser. All the abovementioned options are suported. The difference is only in URL endpoint (without '/api/v1' part):
```
http://127.0.0.1:5000/product/
http://127.0.0.1:5000/product/1
```

## POST method and data validation
The example project utilizes [marshmallow](https://marshmallow.readthedocs.io) framework to serve input data validation.

E.g., schema validation details defined in ProductSchema. If some mandatory data is missed or invalid in POST request, this case will be correctly handled.

Missed Data case:
```
>>> r1 = requests.post('http://127.0.0.1:5000/api/v1/product/', json={'in_store': True})
>>> r1.status_code
400
>>> r1.json()
{'title': ['Missing data for required field.'], 'price_rub': ['Missing data for required field.']}
```
Invalid Data case:
```
>>> r2 = requests.post('http://127.0.0.1:5000/api/v1/product/', json={'title': True, 'price_rub': 'some string'})
>>> r2.status_code
400
>>> r2.json()
{'title': ['Not a valid string.'], 'price_rub': ['Not a valid integer.']}
```
Valid Data case:
```
>>> r3 = requests.post('http://127.0.0.1:5000/api/v1/product/', json={'title': 'test2', 'price_rub': 12300})
>>> r3.status_code
200
>>> r3.json()
'ok'
```