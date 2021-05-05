from flask_restful import Resource


class Catalogue(Resource):
    def get(self):
        return 'catalog'
