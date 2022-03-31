from pytest import mark, raises
import requests
from tests.helpers.helper import response_is_not_empty


def test_when_consult_saraiva_with_description():
    json_data = {'url': 'https://www.saraiva.com.br/box-o-essencial-da-psicologia-3-volumes-10081856/p'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


def test_when_consult_saraiva_without_description():
    json_data = {'url': 'https://www.saraiva.com.br/sobre-a-brevidade-da-vida-edicao-especial-com-prefacio-de-lucia-helena-galvao-maya--capa-es-20086735/p'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


@mark.xfail()
def test_when_consult_saraiva_with_wrong_url_must_return_no_data():
    json_data = {'url': 'https://www.saraiva.com.br/Sistema/404?ProductLinkNotFound=sbbbbbbb--capa-es-20086735'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True
