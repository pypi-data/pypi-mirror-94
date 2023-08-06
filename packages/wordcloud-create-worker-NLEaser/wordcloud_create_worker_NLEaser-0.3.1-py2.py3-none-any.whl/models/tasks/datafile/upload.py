import mongoengine as me
import marshmallow as ma

from models.datafile import DataFileModel, DataFileSchema
from models.tasks import TaskModel, TaskSchema
from models.user import UserModel


class DataFileUploadTaskModel(TaskModel):
    meta = {
        'allow_inheritance': True
    }

    task_name = me.fields.StringField(default="datafile_import")
    datafile: DataFileModel = me.fields.ReferenceField(DataFileModel, required=True)


class DataFileUploadTaskSchema(TaskSchema):
    task_name = ma.fields.String(default="datafile_import")
    datafile = ma.fields.String(required=True)

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return DataFileUploadTaskModel(**data)
