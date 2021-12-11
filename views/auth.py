from flask import request
from flask_restx import Resource, Namespace
from implemented import auth_service


auth_ns = Namespace('auth')




@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        tokens = auth_service.create(req_json)
        return tokens, 201

    def put(self):
        req_json = request.json
        tokens = auth_service.update(req_json)
        return tokens, 201