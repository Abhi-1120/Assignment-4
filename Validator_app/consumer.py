import ast
import random
import time
import pika
import requests
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='wotnot', durable=True)


def callback(ch, method, properties, body):
    data = body.decode("utf-8")
    data = ast.literal_eval(data)
    if data['random'] % 10 == 0:
        r = random.randint(0, 60)
        time.sleep(4)
        if r % 10 == 0:
            data['category'] = "Failed"
        else:
            data['category'] = "Retried"
    payload = {
        "data": [
            {
                "id": data['id'],
                "message": data['message'][0],
                "count": data['count'],
                "category": data['category']
            }
        ]
    }
    response = requests.post("http://127.0.0.1:3000/tracker/insert", json=payload)
    print(response.json())
    print(response.status_code)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='wotnot', on_message_callback=callback)
channel.start_consuming()
