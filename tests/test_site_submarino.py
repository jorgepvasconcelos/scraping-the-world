import requests

from tests.helpers.helper import response_is_not_empty


def test_when_consult_submarino_with_description():
    json_data = {'url': 'https://www.submarino.com.br/produto/105016640'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) == True



