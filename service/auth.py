import calendar
import datetime

from flask import request
from flask_restx import abort
from jwt import jwt
from dao.auth import AuthDAO
from dao.model.auth import Auth
from dao.model.user import User
from service.user import UserService
from setup_db import db


secret = 's3cR$eT'
algo = 'HS256'


class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def create(self):
        req_json = request.json
        auth = Auth.query.get(req_json)
        if not auth:
            abort(404)

        user = db.session.query(User).filter(User.username == auth.username).first()

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = UserService.get_hash(auth.password)

        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user.username,
            "role": user.role
        }

        data["exp"] = self.dao.create_experation_date(minutes=30)
        access_token = self.dao.create_token(data, secret, algorithm=algo)
        data["exp"] = self.dao.create_experation_date(days=130)
        refresh_token = self.dao.create_token(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201

    def update(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        try:
            data = jwt.decode(jwt=refresh_token, key=secret, algorithms=[algo])
        except Exception as e:
            abort(400)

        username = data.get("username")

        user = db.session.query(User).filter(User.username == username).first()

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens, 201