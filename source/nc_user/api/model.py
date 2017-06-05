from sqlalchemy_utils import EmailType, UUIDType
from .. import db


class UserModel(db.Model):

    id = db.Column(UUIDType(), primary_key=True)
    e_mail = db.Column(EmailType)
    create_stamp = db.Column(db.DateTime)
    edit_stamp = db.Column(db.DateTime)
