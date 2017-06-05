from . import api_restful
from .resource import *


# - Get all users
# - Post user
api_restful.add_resource(UsersResource,
    "/users",
    endpoint="users")


# - Get user by user-id
api_restful.add_resource(UserResource,
    "/users/<uuid:user_id>",
    endpoint="user")
