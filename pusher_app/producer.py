from flask import Flask
from flask_restful import Resource, Api
import pika
from flask_jwt_extended import jwt_required, JWTManager
import jwt
import random

app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.secret_key = 'Abhi'
jwt_manager = JWTManager(app)

data = {
    "id": 5,
    "name": "Abhi Bhalani",
    "message": "Hello World1",
    "random": random.randint(0, 60),
    "counter": ""
}


class HelloWorld(Resource):
    @jwt_required()
    def get(self, data=data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='python', durable=True)
        channel.basic_publish(
            exchange='test',
            routing_key='Abhi',
            body=str(data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        connection.close()
        token = jwt.encode(payload=data, key="Abhi")
        data = jwt.decode(token, "Abhi", algorithms=["HS256"])
        return data


api.add_resource(HelloWorld, '/get')

if __name__ == '__main__':
    app.run(port=5000)
