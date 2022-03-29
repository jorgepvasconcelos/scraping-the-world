import requests
from requests_html import HTMLSession
session = HTMLSession()

url = 'https://www.saraiva.com.br/box-o-essencial-da-psicologia-3-volumes-10081856/p'


response = session.get(url)
response.html.render(reload=True)
# response = requests.get(url=url)

print(response.text)