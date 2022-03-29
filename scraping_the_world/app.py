from flask import Flask
from flask_restful import Api

from scraping_the_world.models.utils import create_database
from routes.index import Index
from routes.consult import Consult
from env import ENV


app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/')
api.add_resource(Consult, '/consult')


if __name__ == '__main__':
    create_database()
    app.run(debug=False, host='0.0.0.0', port=5000)
