# py_webapi_flask_example
Simple example of the wsgi-compatible API web app using Flask framework

# Setup
Once you've cloned the repo from GitHub, make sure you've created a virtual environment for experiments.
```
sudo pip3 install virtualenv
python3 -m virtualenv ./venv
source venv/bin/activate
```
Now you can install some dependencies:
```
pip3 install flask marshmallow
```
# Usage
Simply run the server:
```
python server.py
```
Now open browser and try the following API routes:
```
http://127.0.0.1:8080/api/v1/products/?q=iphone
http://127.0.0.1:8080/api/v1/products/?from=0&to=2
```
Note on the params stated after ? symbol in URL.

They are defined in endpoints.py, whilst the fetched data are from db.py

## POST method and data validation
The example project utilizes [marshmallow](https://marshmallow.readthedocs.io) framework to serve input data validation.

E.g., schema validation details defined in ProductSchema. If some mandatory data is missed or invalid in POST request, this case will be correctly handled.

Missed Data case:
```
>>> r1 = requests.post('http://127.0.0.1:8080/api/v1/products/', json={'title': 'test'})
>>> r1.status_code
400
>>> r1.json()
{'price_rub': ['Missing data for required field.']}
```
Valid Data case:
```
>>> r2 = requests.post('http://127.0.0.1:8080/api/v1/products/', json={'title': 'test2', 'price_rub': 12300})
>>> r2.status_code
200
>>> r2.json()
'ok'
```