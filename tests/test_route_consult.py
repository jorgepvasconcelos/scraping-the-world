import requests


def test_when_consult_receive_not_implemented_scraping_site_must_return_404_status_code():
    json_data = {'url': 'https://http.cat/'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data)

    assert response.status_code == 404










