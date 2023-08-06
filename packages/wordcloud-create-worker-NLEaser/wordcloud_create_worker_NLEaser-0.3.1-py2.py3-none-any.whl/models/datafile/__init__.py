import datetime
import mongoengine as me
import marshmallow as ma

from models.user import UserModel, UserSchema


class DataFileModel(me.Document):
    meta = {
        'collection': 'datafile'
    }

    owner = me.fields.ReferenceField(UserModel)
    name = me.fields.StringField()
    format = me.fields.StringField(required=True, choices=['csv', 'xlsx', 'txt'])
    language = me.fields.StringField(required=True, choices=["portuguese", "english"])
    text_column = me.fields.StringField(required=True)
    created_at = me.fields.DateTimeField(default=datetime.datetime.now)
    excluded = me.fields.BooleanField(default=False)


class DataFileSchema(ma.Schema):
    id = ma.fields.String(required=True, dump_only=True)
    name = ma.fields.String()
    format = ma.fields.String(required=True)
    language = ma.fields.String(required=True)
    text_column = ma.fields.String(required=True)
    created_at = ma.fields.DateTime(default=datetime.datetime.now)
    excluded = ma.fields.Boolean(default=False)

    @ma.post_load()
    def make_data_file(self, data, **kwargs):
        return DataFileModel(**data)
