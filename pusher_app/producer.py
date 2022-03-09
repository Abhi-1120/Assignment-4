import pika
import jwt
import random
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, JWTManager


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.secret_key = 'Abhi'
api = Api(app)
jwt_manager = JWTManager(app)

data = {
    "id": 5,
    "name": "Abhi Bhalani",
    "message": "Hello World1",
    "random": random.randint(0, 60),
    "counter": ""
}


class HelloWorld(Resource):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='wotnot', durable=True)

    @jwt_required()
    def get(self, data=data):
        self.channel.basic_publish(exchange='test-wotnot', routing_key='python', body=str(data),
                                   properties=pika.BasicProperties(delivery_mode=2, ))
        self.connection.close()
        token = jwt.encode(payload=data, key="Abhi")
        data = jwt.decode(token, "Abhi", algorithms=["HS256"])
        return data


api.add_resource(HelloWorld, '/get')

if __name__ == '__main__':
    app.run(port=5000)
