from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from src import db, BaseMixin, ReprMixin


class User(BaseMixin, db.Model, ReprMixin):
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    last_login_at = db.Column(db.DateTime())
    mobile_number = db.Column(db.String(10), unique=True, index=True)

    roles = db.relationship('Role', back_populates='users', secondary='user_role')
    user_profile = db.relationship("UserProfile", back_populates="user",
                                   uselist=False, cascade='all, delete-orphan',
                                   lazy='select')
    comments = db.relationship('Comment', back_populates='commenter', uselist=True,
                               lazy='dynamic')
    ratings = db.relationship('UserRating', back_populates='rater', uselist=True,
                              lazy='dynamic')

    @hybrid_property
    def name(self):
        return '{}'.format(self.user_profile.first_name) + (' {}'.format(self.user_profile.last_name) if
                                               self.user_profile.last_name else '')


class UserProfile(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['id', 'first_name']

    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40))
    profile_picture = db.Column(db.Text())
    bio = db.Column(db.Text())
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('male', 'female', 'other', name='varchar'))
    marital_status = db.Column(db.Enum('single', 'married', 'divorced', 'widowed', name='varchar'))
    education = db.Column(db.Enum('undergraduate', 'graduate', 'post_graduate', name='varchar'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, index=True)

    user = db.relationship('User', back_populates="user_profile", single_parent=True)


class Role(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text, unique=True)

    users = db.relationship('User', secondary='user_role', back_populates='roles')


class UserRole(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['user_id', 'role_id']

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', foreign_keys=[role_id])
    user = db.relationship('User', foreign_keys=[user_id])

    UniqueConstraint(role_id, user_id, 'role_user_un')
