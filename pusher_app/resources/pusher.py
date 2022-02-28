from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required


class Userdata(Resource):
    @jwt_required()
    def get(self):
        pass


