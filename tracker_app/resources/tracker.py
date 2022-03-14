from datetime import datetime
from flask import request
from flask_restful import Resource
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch([{"scheme": "http", "host": "localhost", "port": 9200}])


class Tracker(Resource):
    def get(self):
        payload = request.json
        data = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "wildcard": {
                                "message": {
                                    "value": "*" + payload['message'].lower() + "*"
                                }
                            }
                        }
                    ]
                }
            }
        }
        res = es.search(index="tracker", body=data, size=1000)
        return res['hits']['hits']


class TrackerCount(Resource):
    def get(self):
        payload = request.json
        data = []
        data = {
            "aggs": {
                "category": {
                    "terms": {
                        "field": "category.keyword"
                    }
                },
                "created_at": {
                    "terms": {
                        "field": "created_at"
                    }
                }
            }
        }
        res = es.search(index="tracker", body=data)
        return res['aggregations']


class TrackerInsert(Resource):
    def post(self):
        payload = request.json
        index = "tracker"
        data = []
        for item in payload['data']:
            data.append(
                {
                    "_index": index,
                    "_type": "_doc",
                    "_source": {
                        "id": item['id'],
                        "message": item["message"],
                        "count": item['count'],
                        "category": item["category"],
                        "created_at": datetime.now()
                    }
                }
            )
        res = helpers.bulk(es, data)
        if res:
            return {"ok": True}
        else:
            return {"ok": False}
