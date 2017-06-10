from flask_jwt import JWT,JWTError, jwt_required
from flask_restful import Resource, reqparse, Api
from flask import app, jsonify, redirect
from model.customer import Customer
from model.user_token import *
from werkzeug.security import safe_str_cmp
from collections import OrderedDict
import mlab
import datetime
from datetime import date



class LoginCredentials(Resource):
    def __init__(self,id,username, password):
        self.id = id;
        self.username = username;
        self.password = password;

    def authenticate(username, password):
        for user in Customer.objects(username=username):
            if user.password == password:
                return LoginCredentials(str(user.id),user.username,user.password)

    def identity(payload):
        user_id = payload["identity"]
        user = Customer.objects().with_id(user_id)
        if (user_id is not None):
            return LoginCredentials(str(user.id),user.username, user.password)

def handle_user_exception_again(e):
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e

class RegisterRes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="username", type=str, location="json")
        parser.add_argument(name="password", type=str, location="json")
        body = parser.parse_args()
        username = body.username
        password = body.password
        print("REGISTER SAVE")
        if username is None or password is None:
            return {"meassage":"Thiếu trường"},401

        found_user = Customer.objects(username = username).first()
        if found_user is not None:
            print("User already exist")
            return redirect('api/login',307)

        user = Customer(username = username, password = password)
        print({"name": user.username+";password:"+user.password})
        user.save()

        return redirect('api/login', 307)

    def get(self):
        print("get all user")
        customer = Customer.objects()
        return mlab.list2json(customer), 200

def authenticate(username, password):
    print("Authenticate register")
    for user in Customer.objects(username=username):
        if user.password == password:
            if safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
                print("OK")
                return LoginCredentials(str(user.id), user.username, user.password)


def identity(payload):
    print("Identity register")
    user_id = payload['identity']
    user = Customer.objects.with_id(user_id)
    if user is not None:
        return LoginCredentials(str(user.id), user.username, user.password)

def jwt_init(app):
    app.config['SECRET_KEY'] = 'khanh'
    app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(hours=24)
    app.config["JWT_AUTH_URL_RULE"] = "/api/login"
    app.handle_user_exception = handle_user_exception_again
    jwt = JWT(app=app,
              authentication_handler=authenticate,
              identity_handler=identity)
    return jwt
