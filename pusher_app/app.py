from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.pusher import Userdata

app = Flask(__name__)
api = Api(app)

api.add_resource(Userdata, '/push_user')

if __name__ == '__main__':
    app.run(debug=True)
