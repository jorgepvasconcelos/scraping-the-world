from flask_restful import Resource


class Consult(Resource):
    def get(self):
        return 'Consult'
