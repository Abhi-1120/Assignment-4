import pika
import jwt
import random

import redis
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['SECRET_KEY'] = 'Abhi'
api = Api(app)

r = redis.StrictRedis(host='localhost', port=6379, password='')
jwt_manager = JWTManager(app)


class HelloWorld(Resource):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='wotnot', durable=True)
        self.headers = request.headers['Authorization']
        self.Token = self.headers.split(" ")

    @jwt_required()
    def post(self):
        current_identity = get_jwt_identity()
        payload = request.json
        r_get = r.get("{id}_user".format(id=current_identity))
        redis = r.hincrby(r_get, 'count', 1)
        print(redis)

        data = {
            "id": current_identity,
            "message": payload['message'],
            "random": random.randint(0, 60),
            "category": "Direct",
            "count": redis
        }
        print(data)
        if current_identity:
            self.channel.basic_publish(exchange='test-wotnot', routing_key='python', body=str(data),
                                       properties=pika.BasicProperties(delivery_mode=2, ))

        self.connection.close()
        token = jwt.decode(self.Token[1], "Abhi", algorithms=["HS256"])
        return {"ok": True}


api.add_resource(HelloWorld, '/post')

if __name__ == '__main__':
    app.run(port=5000)
