from flask import Flask
from flask_restful import Api

from routes.index import Index


app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
