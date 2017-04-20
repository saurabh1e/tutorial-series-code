from flask_restful import Resource
from flask import make_response, jsonify, request
from src import api, db
from .models import User
from .schemas import UserSchema


class UserResource(Resource):

    model = User
    schema = UserSchema

    def get(self, slug):
        user = self.model.query.get(slug)
        if not user:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(user).data), 200)

    def patch(self, slug):
        user = self.model.query.get(slug)
        if not user:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        user, errors = self.schema().load(request.json, instance=user)
        if errors:
            return make_response(jsonify(errors), 400)
        db.session.commit()
        return make_response(jsonify(self.schema().dump(user).data), 200)

    def delete(self, slug):
        user = self.model.query.get(slug)
        if not user:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({}), 204)


class UserListResource(Resource):

    model = User
    schema = UserSchema

    def get(self):
        users = self.model.query.limit(20).all()
        if not users:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(users, many=True).data), 200)

    def post(self):
        users, errors = self.schema().load(request.json, many=True)
        if errors:
            return make_response(jsonify(errors), 400)
        else:
            db.session.add_all(users)
            db.session.commit()
            return make_response(jsonify(self.schema().dump(users, many=True).data), 201)

api.add_resource(UserResource, '/user/<slug>', endpoint='user')
api.add_resource(UserListResource, '/user', endpoint='users')

