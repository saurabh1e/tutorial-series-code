from src import ma, BaseSchema
from .models import User, UserProfile


class UserSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ('password',)

    id = ma.Integer(dump_only=True)
    email = ma.Email(require=True)
    mobile_number = ma.String(require=True, max=10, min=10)
    user_profile = ma.Nested('UserProfileSchema', many=False, load=True)


class UserProfileSchema(BaseSchema):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    id = ma.Integer(load=True, partial=True)
    first_name = ma.String()
    last_name = ma.String()
    user_id = ma.Integer(load_only=True, partial=True)
