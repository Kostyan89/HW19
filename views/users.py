from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')
user_schema = UserSchema()


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        new_user = user_service.create(req_json)
        return user_schema.dump(new_user), 201


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def put(self, uid: int):
        req_json = request.json
        updated_user = user_service.filter_by(uid).update(req_json)
        return user_schema.dump(updated_user), 204

    def delete(self, uid: int):
        user_service.delete(uid)
        return "", 204