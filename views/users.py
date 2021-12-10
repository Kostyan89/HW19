from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200