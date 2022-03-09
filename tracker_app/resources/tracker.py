from flask_restful import Resource
from datetime import datetime
from elasticsearch import Elasticsearch, helpers


es = Elasticsearch([{"scheme": "http", "host": "localhost", "port": 9200}])


class Tracker(Resource):
    def post(self):
        doc = {
            "id": 5,
            "name": "Abhi Patel",
            "message": "Hello World1",
            "category": "category",
            "created_at": datetime.now()
        }
        resp = es.index(index="tracker", document=doc)
        return resp['result']

    def get(self):
        data = {
            "_source": ["message"],
            "query": {
                "match_all": {}
            }
        }
        res = es.search(index="tracker", body=data, size=1000)
        return res['hits']['hits']


class TrackerCount(Resource):
    def get(self):
        data = {
            "query": {
                "match": {
                    "category": "Failed"
                },
            }
        }
        res = es.count(index="tracker", body=data)
        return res['count']


class TrackerInsert(Resource):
    def get(self):
        data = [
            {
                "_index": "tracker",
                "_type": "_doc",
                "_id": j,
                "_source": {
                    "id": 1+j,
                    "name": "Abhi",
                    "message": "Hello",
                    "category": "Direct",
                    "created_at": datetime.now()
                }
            }
            for j in range(10, 20)
        ]
        res = helpers.bulk(es, data)
        return res
