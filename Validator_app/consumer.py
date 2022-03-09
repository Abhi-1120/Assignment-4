import requests
from flask import Flask
from flask_restful import Api
import pika
import random
import time


app = Flask(__name__)
api = Api(app)
app.config['DEBUG'] = True


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='python', durable=True)

    def callback(ch, method, properties, body):
        data = body.decode("utf-8")
        print(data)
        if 11 % 10 == 0:
            r = random.randint(0, 60)
            time.sleep(4)
            if r % 10 == 0:
                print("Failed")
            else:
                print("Retried")
        else:
            print("Direct")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.start_consuming()


if __name__ == '__main__':
    main()
