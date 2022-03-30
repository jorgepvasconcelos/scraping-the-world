import requests

from tests.helpers.helper import response_is_not_empty


def test_when_consult_americanas_with_description():
    json_data = {'url': 'https://www.americanas.com.br/produto/2896992161'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) == True


def test_when_consult_americanas_without_description():
    json_data = {'url': 'https://www.americanas.com.br/produto/3068486001'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) == True
