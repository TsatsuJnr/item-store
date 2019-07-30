from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item needs a store Id!"
                        )

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.to_json()
        return {'responseCode': '400', 'responseMessage': 'Item {} Not Found'.format(name)}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'responseCode': 400, 'responseMessage': 'An item with name {} already exists.'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)
        try:
            item.save()
        except:
            return {'responseCode': '100', 'responseMessage': 'Data Access Exception'}, 500
        return item.to_json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'responseCode': '200', 'responseMessage': 'Item {} deleted'.format(name)}
        return {'responseCode': '404', 'responseMessage': 'Item {} does not exist'.format(name)}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {'responseCode': '100', 'responseMessage': 'Data Access Exception'}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'responseCode': '100', 'responseMessage': 'Data Access Exception'}, 500
        item.save()
        return item.to_json()


class Items(Resource):
    def get(self):
        return{'items': [item.to_json() for item in ItemModel.query.all()]}
