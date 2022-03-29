import requests


def test_when_consult_americanas_with_description():
    json_data = {'url': 'https://www.americanas.com.br/produto/2896992161'}
    response = requests.get(url='http://localhost:5000/consult', json=json_data).json()
    valid_response = {'titulo': 'Fone de Ouvido Wireless Bluetooth InPods 12 Preto',
                      'imagem': 'https://images-americanas.b2w.io/produtos/2896992161/imagens/fone-de-ouvido-wireless-bluetooth-inpods-12-preto/2896992161_1_large.jpg',
                      'preco': 'R$ 37,50',
                      'descricao': 'O par de fones de ouvido inPods 12 une o que há de tecnologia e sofisticação, não abrindo mão do design perfeito multicolorido. Este fone tws (True wireless stereo) possui versão do bluetooth V5.0 de alta velocidade de transferência...',
                      'url': 'https://www.americanas.com.br/produto/2896992161'}
    assert valid_response == response



