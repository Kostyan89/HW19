from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from helpers import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')
genre_schema = GenreSchema()

@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        new_genre = genre_service.create(req_json)
        return genre_schema.dump(new_genre), 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid: int):
        req_json = request.json
        updated_genre = genre_service.filter_by(gid).update(req_json)
        return genre_schema.dump(updated_genre), 204

    @admin_required
    def delete(self, gid: int):
        genre_service.delete(gid)
        return "", 204