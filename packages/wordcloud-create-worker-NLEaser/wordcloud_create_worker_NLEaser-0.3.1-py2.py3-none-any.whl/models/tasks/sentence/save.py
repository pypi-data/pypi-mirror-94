import mongoengine as me
import marshmallow as ma

from models.tasks.datafile.upload import DataFileUploadTaskModel, DataFileUploadTaskSchema


class SentenceSaveTaskModel(DataFileUploadTaskModel):
    task_name = me.fields.StringField(default="sentence_import")
    parent: DataFileUploadTaskModel = me.fields.ReferenceField(DataFileUploadTaskModel, required=True)
    content = me.fields.StringField(required=True)
    index = me.fields.IntField(required=True)


class SentenceSaveTaskSchema(DataFileUploadTaskSchema):
    parent = ma.fields.String(required=True)
    content = ma.fields.String(required=True)
    index = ma.fields.Integer(required=True)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return SentenceSaveTaskModel(**data)
