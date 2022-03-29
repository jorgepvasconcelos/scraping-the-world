from urllib.parse import urlparse

from flask_restful import Resource, reqparse

from scraping_the_world.scrapers.americanas import scraping_americanas


def get_data(url):
    parse = urlparse(url)
    hostname = parse.hostname

    if 'americanas' in hostname:
        result = scraping_americanas(url)
        return result


class Consult(Resource):
    params = reqparse.RequestParser()
    params.add_argument('url', type=str, required=True, help="The field 'url' cannot be left blank.")

    def get(self):
        request_data = Consult.params.parse_args()
        print(request_data)

        result = get_data(request_data['url'])
        print(result)

        json_return = {
            'titulo': 'esse e o titulo',
            'imagem': 'esse e a imagem',
            'preco': 'esse e o preco',
            'url': 'esse e a url',
        }
        return json_return
