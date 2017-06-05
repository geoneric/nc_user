import datetime
import uuid
from marshmallow import fields, post_dump, post_load, pre_load, ValidationError
from marshmallow.validate import Length, OneOf
from .. import ma
from .model import UserModel


class UserSchema(ma.Schema):

    class Meta:
        # Fields to include in the serialized result.
        fields = ("id", "e_mail", "_links")

    id = fields.UUID(required=True)
    e_mail = fields.Email(required=True)
    create_stamp = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())
    edit_stamp = fields.DateTime(dump_only=True,
        missing=datetime.datetime.utcnow().isoformat())

    _links = ma.Hyperlinks({
        "self": ma.URLFor("api.user", user_id="<id>"),
        "collection": ma.URLFor("api.users")

        # TODO Add links to other resources
    })


    def key(self,
            many):
        return "users" if many else "user"


    @pre_load(
        pass_many=True)
    def unwrap(self,
            data,
            many):
        key = self.key(many)

        if key not in data:
            raise ValidationError(
                "Input data must have a {} key".format(key))

        return data[key]


    @post_dump(
        pass_many=True)
    def wrap(self,
            data,
            many):

        key = self.key(many)

        return {
            key: data
        }


    @post_load
    def make_object(self,
            data):

        return UserModel(
            id=data["id"],
            e_mail=data["e_mail"],
            create_stamp=datetime.datetime.utcnow(),
            edit_stamp=datetime.datetime.utcnow()
        )
