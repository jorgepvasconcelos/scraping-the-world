from pytest import mark, raises
import requests
from tests.helpers.helper import response_is_not_empty


def test_when_consult_magazineluiza_without_description_1():
    json_data = {'url': 'https://www.magazineluiza.com.br/papel-fotografico-a4-180g-glossy-branco-brilhante-resistente-a-agua-100-folhas-premium/p/ke2bb2cj82/cf/ppft/'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


def test_when_consult_magazineluiza_without_description_2():
    json_data = {'url': 'https://www.magazineluiza.com.br/hd-desktop-seagate-ironwolf-8tb-sistemas-de-backup-nas-sata6-7200rpm-256mb-st8000vn004/p/ghhb06b14b/in/armt/?&seller_id=gigantec'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True


@mark.xfail()
def test_when_consult_magazineluiza_with_wrong_url_must_return_no_data():
    json_data = {'url': 'https://www.magazineluiza.com.br/tv-4dddddk-ulddtra-hd/tv-ddddde-vidsseo/ss/sset/tv4444k/'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) is True
