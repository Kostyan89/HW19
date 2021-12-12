from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.auth import AuthSchema
from implemented import auth_service


auth_ns = Namespace('auth')
auth_schema = AuthSchema()



@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        auth = AuthSchema().load(req_json)
        if auth is None:
            abort(400)
        tokens = auth_service.create(req_json)
        return tokens, 201

    def put(self):
        req_json = request.json
        auth = AuthSchema().load(req_json)
        if auth is None:
            abort(400)
        tokens = auth_service.update(req_json)
        return tokens, 201