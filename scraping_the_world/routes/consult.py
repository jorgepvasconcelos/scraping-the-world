from urllib.parse import urlparse

from flask_restful import Resource, reqparse

from scraping_the_world.scrapers.americanas import scraping_americanas


def have_to_redo(data_dict: dict) -> bool:
    for value in data_dict.values():
        print(value)
        if value is None:
            break
        return False
    return True


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

        for _ in range(3):
            result = get_data(request_data['url'])
            if have_to_redo(result):
                continue
            else:
                break

        titulo = result['titulo']
        imagem = result['imagem']
        preco = result['preco']
        url = result['url']

        json_return = {
            'titulo': titulo,
            'imagem': imagem,
            'preco': preco,
            'url': url,
        }
        return json_return
