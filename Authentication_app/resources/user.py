import json
import redis
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from Authentication_app.models.user import UserModel
from Authentication_app.schema.user import UserSchema

user_schema = UserSchema()

r = redis.Redis(host='localhost', port=6379, password='')


class UserRegister(Resource):
    def post(self):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        if UserModel.find_by_name(user.username):
            return {"message": "USER_ALREADY_EXISTS"}, 400
        elif 5 > len(user.username):
            return {"message": "Username must be greater than 5 and less than 15"}, 400
        elif 6 > len(user.password):
            return {"message": "Password must be greater than 6 and less than 12"}, 400
        else:
            user.save_to_db()

        data = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "count": 0
        }
        u = json.dumps(data)
        redis = r.set("{id}_user".format(id=user.id), u)
        return {'message': 'User haas been created successfully'}, 201


class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "USER_NOT_FOUND"}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required()
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "USER_NOT_FOUND"}, 404
        user.delete_from_db()
        return {"message": "USER_DELETED"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            user_json = request.get_json()
            user_detail = json.dumps(user_json)
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_name(user_data.username)
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200
