from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.to_json()
        return {'responseCode': '404', 'responseMessage': 'Store {} Not Found'.format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'responseCode': 400, 'responseMessage': 'An item with name {} already exists.'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save()
        except:
            return {'responseCode': '100', 'responseMessage': 'Data Access Exception'}, 500
        return store.to_json(), 201

    def delete(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            item.delete()
            return {'responseCode': '200', 'responseMessage': 'Item {} deleted'.format(name)}
        return {'responseCode': '404', 'responseMessage': 'Item {} does not exist'.format(name)}, 404


class Stores(Resource):
    def get(self):
        return{'stores': [store.to_json() for store in StoreModel.query.all()]}
