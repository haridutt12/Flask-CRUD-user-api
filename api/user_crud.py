from flask import Flask, request, jsonify
from flask_sqlalchemy import  SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_httpauth import  HTTPBasicAuth
from flask import Blueprint

db = SQLAlchemy()
ma = Marshmallow()
auth = HTTPBasicAuth()


api = Blueprint("api", "/v0")

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'crud.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.register_blueprint(api)
    db.init_app(app)
    ma.init_app(app)
    
    return app



class User(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)


    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')



# endpoint to get all users or create a new user
@api.route("/users", methods=["POST", "GET"])
@auth.login_required
def add_user():
    if request.method == "POST":
        username = request.json['username']
        email = request.json['email']

        if User.query.filter_by(username = username).first():
            return '{"err":"user already exist"}', 400

        new_user = User(username, email)

        db.session.add(new_user)
        db.session.commit()

        return UserSchema().jsonify(new_user)

    all_users = User.query.all()
    return UserSchema(many=True).jsonify(all_users)
    

# endpoint to get/put/delete user detail by id
@api.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def user_detail(id):
    user = User.query.get(id)

    if user == None:
        return "user dosen't exist", 404

    if request.method == "GET":
        return UserSchema().jsonify(user)
    
    elif request.method == "PUT":
        username = request.json["username"]
        email = request.json["email"]
        user.username = username
        user.email = email
        db.session.commit()
        return UserSchema().jsonify(user)

    db.session.delete(user)
    db.session.commit()
    return UserSchema().jsonify(user)

# handler for resource not found
@api.errorhandler(404)
def page_not_found(e):
    return "<h1>{}</h1><p>The resource could not be found.</p>".format(404)


@auth.verify_password
def verify_password(username, password):
    if username == "admin" and password == "password":
        return True
    return False


if __name__=='__main__':
    app = create_app()
    app.run(debug=True)
