from datetime import datetime
from urllib.parse import urlparse
from flask_restful import Resource, reqparse

from scraping_the_world.models.utils import DataBase
from scraping_the_world.scrapers.americanas import scraping_americanas
from scraping_the_world.scrapers.submarino import scraping_submarino


def have_to_redo(data_dict: dict) -> bool:
    for value in data_dict.values():
        print(value)
        if value is None:
            break
        return False
    return True


def have_to_update_data(last_verify) -> bool:
    """if have passed one hour of the last_verify in site, must update the datas"""
    actual_hour = datetime.now()
    actual_hour = f'{actual_hour.year}-{actual_hour.month}-{actual_hour.day} {actual_hour.hour}:{actual_hour.minute}:{actual_hour.second}'
    actual_hour = datetime.strptime(actual_hour, "%Y-%m-%d %H:%M:%S")

    time_diff = abs((actual_hour - last_verify).seconds) / 3600
    print('time_diff=', time_diff)
    if time_diff > 1:
        return True
    return False


def get_data(url_site) -> dict:
    data_from_site = {'titulo': None, 'imagem': None, 'preco': None, 'descricao': None, 'url': None}

    for _ in range(3):
        data_from_site = get_data_from_site(url_site)
        if have_to_redo(data_from_site):
            continue
        else:
            break
    return data_from_site


def last_information_get(last_data: dict):
    titulo = last_data['titulo']
    imagem = last_data['imagem']
    preco = last_data['preco']
    descricao = last_data['descricao']
    url = last_data['url_site']

    json_return = {
        'titulo': titulo,
        'imagem': imagem,
        'preco': preco,
        'descricao': descricao,
        'url': url,
    }
    return json_return


def get_data_from_site(url):
    parse = urlparse(url)
    hostname = parse.hostname

    if 'americanas' in hostname:
        result = scraping_americanas(url)
        return result
    elif 'submarino' in hostname:
        result = scraping_submarino(url)
        return result


class Consult(Resource):
    params = reqparse.RequestParser()
    params.add_argument('url', type=str, required=True, help="The field 'url' cannot be left blank.")

    def get(self):
        request_data = Consult.params.parse_args()
        url_received = request_data['url']

        query_result = DataBase.consult_one(query='select * from sites_data where url_recebida = %s', arguments=[url_received])
        if query_result and not have_to_update_data(last_verify=query_result['data_verificado']):
            return last_information_get(last_data=query_result)

        data = get_data(url_received)

        titulo = data['titulo']
        imagem = data['imagem']
        preco = data['preco']
        descricao = data['descricao']
        url = data['url']

        query = """
        INSERT INTO sites_data (titulo, preco, imagem, descricao, url_recebida, url_site)
        VALUES (%s,%s,%s,%s,%s,%s);"""
        DataBase.execute(query=query, arguments=[titulo, preco, imagem, descricao, url_received, url])

        json_return = {
            'titulo': titulo,
            'imagem': imagem,
            'preco': preco,
            'descricao': descricao,
            'url': url,
        }
        return json_return
