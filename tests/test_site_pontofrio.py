import requests

from tests.helpers.helper import response_is_not_empty


def test_when_consult_submarino_without_description_1():
    json_data = {'url': 'https://www.pontofrio.com.br/rack-136-madetec-lisboa-para-tv-ate-50/p/11996540'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) == True


def test_when_consult_submarino_without_description_2():
    json_data = {'url': 'https://www.pontofrio.com.br/refrigerador-electrolux-duplex-dc35a-260l-branco/p/1743666'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()

    assert response_is_not_empty(response) == True
