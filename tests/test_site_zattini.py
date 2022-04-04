from pytest import mark, raises
import requests
from tests.helpers.helper import response_is_not_empty


def test_when_consult_zattini_with_description_1():
    json_data = {'url': 'https://www.zattini.com.br/tenis-reserva-vela-masculino-preto+branco-B67-5119-026'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


def test_when_consult_zattini_with_description_2():
    json_data = {'url': 'https://www.zattini.com.br/scarpin-griffe-salto-medio-bloco-bico-fino-no-bege-BAV-0337-004'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


@mark.xfail()
def test_when_consult_zattini_with_wrong_url_must_return_no_data():
    json_data = {'url': 'https://www.zattini.com.br/tenis-reserva-vela-masculino-preto+br55anco-B67-511966666-026'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True
