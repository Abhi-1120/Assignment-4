from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from ma import ma
from db import db
from resources.user import User, UserRegister, UserLogin

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
app.secret_key = "Abhi"


@app.before_first_request
def create_tables():
    if __name__ == '__main__':
        db.create_all()


jwt = JWTManager(app)

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True, port=5001)
