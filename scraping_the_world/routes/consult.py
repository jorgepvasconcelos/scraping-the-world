from flask_restful import Resource, reqparse


class Consult(Resource):
    params = reqparse.RequestParser()
    params.add_argument('url', type=str, required=True, help="The field 'url' cannot be left blank.")

    def get(self):
        request_data = Consult.params.parse_args()
        print(request_data)
        json_return = {
            'titulo': 'esse e o titulo',
            'imagem': 'esse e a imagem',
            'preco': 'esse e o preco',
            'url': 'esse e a url',
        }
        return json_return
