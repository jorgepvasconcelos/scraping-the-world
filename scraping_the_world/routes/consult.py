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


def get_data(url_site) -> dict:
    data_from_site = {'titulo': None, 'imagem': None, 'preco': None, 'url': None}
    for _ in range(3):
        data_from_site = get_data_from_site(url_site)
        if have_to_redo(data_from_site):
            continue
        else:
            break
    return data_from_site


def get_data_from_site(url):
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

        data = get_data(request_data['url'])

        titulo = data['titulo']
        imagem = data['imagem']
        preco = data['preco']
        url = data['url']

        json_return = {
            'titulo': titulo,
            'imagem': imagem,
            'preco': preco,
            'url': url,
        }
        return json_return
