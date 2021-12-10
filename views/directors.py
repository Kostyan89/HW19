from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')
director_schema = DirectorSchema()

@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        new_director = director_service.create(req_json)
        return director_schema.dump(new_director), 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        r = director_service.get_one(did)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    def put(self, did: int):
        req_json = request.json
        updated_director = director_service.filter_by(did).update(req_json)
        return director_schema.dump(updated_director), 204

    def delete(self, did: int):
        director_service.delete(did)
        return "", 204
