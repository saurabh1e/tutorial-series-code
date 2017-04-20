import os
import re

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import func, select, UniqueConstraint
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'test.db'))
db = SQLAlchemy(app)
ma = Marshmallow(app)


def to_underscore(name):

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class BaseMixin(object):

    @declared_attr
    def __tablename__(self):
        return to_underscore(self.__name__)

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_on = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_on = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())


class ReprMixin(object):

    __repr_fields__ = ['id', 'name']

    def __repr__(self):
        fields = {f: getattr(self, f, '<BLANK>') for f in self.__repr_fields__}
        pattern = ['{0}={{{0}}}'.format(f) for f in self.__repr_fields__]
        pattern = ' '.join(pattern)
        pattern = pattern.format(**fields)
        return '<{} {}>'.format(self.__class__.__name__, pattern)


class User(db.Model, BaseMixin, ReprMixin):
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


class UserProfile(db.Model, BaseMixin, ReprMixin):
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


class Role(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text, unique=True)

    users = db.relationship('User', secondary='user_role', back_populates='roles')


class UserRole(db.Model, BaseMixin, ReprMixin):
    __repr_fields__ = ['user_id', 'role_id']

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', foreign_keys=[role_id])
    user = db.relationship('User', foreign_keys=[user_id])

    UniqueConstraint(role_id, user_id, 'role_user_un')


class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ('password',)
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    email = fields.Email(require=True)
    mobile_number = fields.String(require=True, max=10, min=10)
    user_profile = fields.Nested('UserProfileSchema', many=False, load=True)


class UserProfileSchema(ModelSchema):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        sqla_session = db.session

    id = fields.Integer(load=True, partial=True)
    first_name = fields.String()
    last_name = fields.String()
    user_id = fields.Integer(load_only=True, partial=True)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/users', methods=['GET', 'POST'])
def users_view():
    if request.method == 'GET':
        users = User.query.all()
        users_data = UserSchema().dump(users, many=True).data
        return make_response(jsonify(users_data), 200)

    else:
        users, errors = UserSchema().load(request.json, many=True)
        if errors:
            return make_response(jsonify(errors), 400)
        else:
            db.session.add_all(users)
            db.session.commit()
            return make_response(jsonify(UserSchema().dump(users, many=True).data), 201)


@app.route('/user/<int:slug>', methods=['GET', 'PUT', 'DELETE'])
def user_view(slug):
    user = User.query.get(slug)
    if not user:
        return make_response(jsonify({'error': 'Resource not found'}), 404)
    if request.method == 'GET':
        return make_response(jsonify(UserSchema().dump(user).data), 200)
    if request.method == 'PUT':
        user, errors = UserSchema().load(request.json, instance=user)
        if errors:
            return make_response(jsonify(errors), 400)
        db.session.commit()
        return make_response(jsonify(UserSchema().dump(user).data), 200)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({}), 204)
