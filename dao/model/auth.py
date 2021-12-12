from marshmallow import Schema, fields

from setup_db import db


class Auth(db.Model):
    __tablename__ = 'auth'
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))


class AuthValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)