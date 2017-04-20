from sqlalchemy import select, func, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from src import db, BaseMixin, ReprMixin


class Post(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['id', 'slug']

    slug = db.Column(db.String(55), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    data = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

    author = db.relationship('User', single_parent=True, foreign_keys=[author_id])
    ratings = db.relationship('UserRating', back_populates='post', uselist=True,
                              lazy='dynamic')
    comments = db.relationship('Comment', back_populates='post', uselist=True,
                               lazy='dynamic')

    @hybrid_property
    def avg_rating(self):
        return self.ratings.with_entities(func.Avg(UserRating.rating)).filter(UserRating.post_id == self.id).scalar()

    @hybrid_property
    def total_comments(self):
        return self.comments.with_entities(func.Count(Comment.id)).filter(Comment.post_id == self.id).scalar()

    @avg_rating.expression
    def avg_rating(cls):
        return select([func.Avg(UserRating.rating)]).where(cls.id == UserRating.post_id).as_scalar()


class Comment(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['id', 'commented_by']

    data = db.Column(db.Text, nullable=False)
    is_moderated = db.Column(db.Boolean(), default=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)
    commented_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), index=True)

    post = db.relationship('Post', foreign_keys=[post_id], back_populates='comments')
    commenter = db.relationship('User', foreign_keys=[commented_by], back_populates='comments')
    parent_comment = db.relationship('Comment', remote_side='Comment.id')
    children_comment = db.relationship('Comment', remote_side='Comment.parent_comment_id')


class UserRating(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['rating', 'post_id', 'rated_by']

    rating = db.Column(db.SmallInteger, nullable=False)

    rated_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)

    post = db.relationship('Post', back_populates='ratings', foreign_keys=[post_id])
    rater = db.relationship('User', foreign_keys=[rated_by], back_populates='ratings')

    UniqueConstraint(rated_by, post_id, 'user_post_un')

