import datetime
import mongoengine as me
import marshmallow as ma


class UserModel(me.Document):
    meta = {
        'collection': 'user'
    }
    email = me.fields.EmailField(unique=True)
    password = me.fields.StringField(required=True)
    name = me.fields.StringField(max_length=150, required=True)
    created_at = me.fields.DateTimeField(default=datetime.datetime.now)


class UserSchema(ma.Schema):
    id = ma.fields.String(required=True, dump_only=True)
    email = ma.fields.String(required=True)
    password = ma.fields.String(required=True, load_only=True)
    name = ma.fields.String(required=True, max_length=150)
    created_at = ma.fields.DateTime()

    @ma.post_load()
    def make_user(self, data, **kwargs):
        return UserModel(**data)
