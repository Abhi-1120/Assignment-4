from flask_restful import Resource
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch([{"scheme": "http", "host": "localhost", "port": 9200}])


class Tracker(Resource):
    def post(self):
        doc = {
            "id": 5,
            "name": "Abhi Patel",
            "message": "Hello World1",
            "category": "Retried",
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
                    "category": "Direct"
                },
            }
        }
        res = es.count(index="tracker", body=data)
        return res['count']


class TrackerInsert(Resource):
    def insert(self):
        data = [
            {
                "_id": "828ef1361dad4f289de8983e90f7ea96",
                "name": "2020-02-03T14:15:01Z",
                "message": "hello",
                "category": "Direct",
                "created_at": datetime.now()
            }
        ]

        res = es.bulk(es, data, index="tracker")
        return res
