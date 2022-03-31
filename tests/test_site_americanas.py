from pytest import mark, raises
import requests
from tests.helpers.helper import response_is_not_empty


def test_when_consult_americanas_with_description():
    json_data = {'url': 'https://www.americanas.com.br/produto/2896992161'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


def test_when_consult_americanas_without_description():
    json_data = {'url': 'https://www.americanas.com.br/produto/3068486001'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


@mark.xfail()
def test_when_consult_americanas_with_wrong_url_must_return_no_data():
    json_data = {'url': 'https://www.americanas.com.br/produto/30032022'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True
