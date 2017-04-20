from src import ma, BaseSchema
from .models import Post, Comment, UserRating


class PostSchema(BaseSchema):
    class Meta:
        model = Post
        exclude = ('author_id',)

    id = ma.Integer(dump_only=True)

    slug = ma.String(load=True, allow_none=True)
    title = ma.String(load=True, allow_none=False)
    data = ma.String(load=True, allow_none=False)
    author_id = ma.Integer(load=True, allow_none=False)

    avg_rating = ma.Integer()
    total_comments = ma.Integer()

    author = ma.Nested('UserSchema', dump_only=True, many=False)
    ratings = ma.Nested('CommentSchema', dump_only=True, many=True, only=('id', 'rating', 'rater'))
    comments = ma.Nested('UserRatingSchema', dump_only=True, many=True, only=('id', 'comment', 'children_comment',
                                                                              'commenter'))


class CommentSchema(BaseSchema):
    class Meta:
        model = Comment
        exclude = ('user',)

    id = ma.Integer(load=True, partial=True)
    data = ma.String(load=True, allow_none=False)
    is_moderated = ma.String(load=True, allow_none=True)

    post_id = ma.Integer(load=True, allow_none=False)
    commented_by = ma.Integer(load=True, allow_none=False)
    parent_comment_id = ma.Integer(load=True, allow_none=True)

    commenter = ma.Nested('UserSchema', many=False, dump_only=True)

    # parent_comment = ma.Nested('CommentSchema', only=('id',))
    children_comment = ma.Nested('CommentSchema', only=('id', 'comment', 'commenter'))


class UserRatingSchema(BaseSchema):
    class Meta:
        model = UserRating
        exclude = ('user',)

    id = ma.Integer(load=True, partial=True)
    rating = ma.Integer(load=True, allow_none=False)

    rated_by = ma.Integer(load=True, allow_none=False)
    post_id = ma.Integer(load=True, allow_none=False)

    post = ma.Nested('PostSchema', dump_only=True, only=('id',))
    rater = ma.Nested('UserSchema', dump_only=True, only=('id', 'name'))
