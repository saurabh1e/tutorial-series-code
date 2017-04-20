from flask_restful import Resource
from flask import make_response, jsonify, request
from src import api, db
from .models import Post, UserRating, Comment
from .schemas import CommentSchema, PostSchema, UserRatingSchema


class PostResource(Resource):

    model = Post
    schema = PostSchema

    def get(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(post).data), 200)

    def patch(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        post, errors = self.schema().load(request.json, instance=post)
        if errors:
            return make_response(jsonify(errors), 400)
        db.session.commit()
        return make_response(jsonify(self.schema().dump(post).data), 200)

    def delete(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(post)
        db.session.commit()
        return make_response(jsonify({}), 204)


class PostListResource(Resource):

    model = Post
    schema = PostSchema

    def get(self):
        posts = self.model.query.limit(20).all()
        if not posts:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(posts, many=True).data), 200)

    def post(self):
        posts, errors = self.schema().load(request.json, many=True)
        if errors:
            return make_response(jsonify(errors), 400)
        else:
            db.session.add_all(posts)
            db.session.commit()
            return make_response(jsonify(self.schema().dump(posts, many=True).data), 201)

api.add_resource(PostResource, '/post/<slug>', endpoint='post')
api.add_resource(PostListResource, '/post', endpoint='posts')


class CommentResource(Resource):

    model = Comment
    schema = CommentSchema

    def get(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(post).data), 200)

    def patch(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        post, errors = self.schema().load(request.json, instance=post)
        if errors:
            return make_response(jsonify(errors), 400)
        db.session.commit()
        return make_response(jsonify(self.schema().dump(post).data), 200)

    def delete(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(post)
        db.session.commit()
        return make_response(jsonify({}), 204)


class CommentListResource(Resource):

    model = Comment
    schema = CommentSchema

    def get(self):
        posts = self.model.query.limit(20).all()
        if not posts:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(posts, many=True).data), 200)

    def post(self):
        posts, errors = self.schema().load(request.json, many=True)
        if errors:
            return make_response(jsonify(errors), 400)
        else:
            db.session.add_all(posts)
            db.session.commit()
            return make_response(jsonify(self.schema().dump(posts, many=True).data), 201)

api.add_resource(CommentResource, '/comment/<slug>', endpoint='comment')
api.add_resource(CommentListResource, '/comment', endpoint='comments')


class UserRatingResource(Resource):

    model = UserRating
    schema = UserRatingSchema

    def get(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(post).data), 200)

    def patch(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        post, errors = self.schema().load(request.json, instance=post)
        if errors:
            return make_response(jsonify(errors), 400)
        db.session.commit()
        return make_response(jsonify(self.schema().dump(post).data), 200)

    def delete(self, slug):
        post = self.model.query.get(slug)
        if not post:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        db.session.delete(post)
        db.session.commit()
        return make_response(jsonify({}), 204)


class UserRatingListResource(Resource):

    model = UserRating
    schema = UserRatingSchema

    def get(self):
        posts = self.model.query.limit(20).all()
        if not posts:
            return make_response(jsonify({'error': 'Resource not found'}), 404)
        return make_response(jsonify(self.schema().dump(posts, many=True).data), 200)

    def post(self):
        posts, errors = self.schema().load(request.json, many=True)
        if errors:
            return make_response(jsonify(errors), 400)
        else:
            db.session.add_all(posts)
            db.session.commit()
            return make_response(jsonify(self.schema().dump(posts, many=True).data), 201)

api.add_resource(UserRatingResource, '/user_rating/<slug>', endpoint='user_rating')
api.add_resource(UserRatingListResource, '/user_rating', endpoint='user_ratings')
