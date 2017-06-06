from werkzeug.exceptions import *
from flask_restful import Resource
from flask import request
from .. import db
from .model import UserModel
from .schema import UserSchema


user_schema = UserSchema()


class UserResource(Resource):


    def get(self,
            user_id):

        user = UserModel.query.get(user_id)

        if user is None:
            raise BadRequest("User could not be found")


        data, errors = user_schema.dump(user)

        if errors:
            raise InternalServerError(errors)


        return data


    def delete(self,
            user_id):

        user = UserModel.query.get(user_id)

        if user is None:
            raise BadRequest("User could not be found")


        db.session.delete(user)
        db.session.commit()


        # From user to dict representing a user.
        data, errors = user_schema.dump(user)
        assert not errors, errors
        assert isinstance(data, dict), data

        # # Remove links, there is no resource anymore.
        # # TODO Use Marshmallow contexts?
        # del data["user"]["_links"]


        # return data, 200

        return "", 204


class UsersResource(Resource):


    def get(self):

        users = UserModel.query.all()
        data, errors = user_schema.dump(users, many=True)

        if errors:
            raise InternalServerError(errors)

        assert isinstance(data, dict), data


        return data


    def post(self):

        json_data = request.get_json()

        if json_data is None:
            raise BadRequest("No input data provided")


        # Validate and deserialize input.
        user, errors = user_schema.load(json_data)

        if errors:
            raise UnprocessableEntity(errors)


        # Write user to database.
        db.session.add(user)
        db.session.commit()


        # From record in database to dict representing a user.
        data, errors = user_schema.dump(
            UserModel.query.get(user.id))
        assert not errors, errors
        assert isinstance(data, dict), data


        return data, 201
