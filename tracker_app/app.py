from flask import Flask
from flask_restful import Api
from resources.tracker import Tracker, TrackerCount, TrackerInsert

app = Flask(__name__)
api = Api(app)


api.add_resource(Tracker, '/tracker')
api.add_resource(TrackerCount, '/tracker/count')
api.add_resource(TrackerInsert, '/tracker/insert')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
