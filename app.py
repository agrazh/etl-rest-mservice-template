from flask import Flask, request
from flask_restful import Resource, Api

items = []

app = Flask(__name__)
api = Api(app)

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with a name '{}' already exists.".format(name)}, 400

        data = request.get_json() # force=False, silent=False
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'item': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=4000, debug=True)
