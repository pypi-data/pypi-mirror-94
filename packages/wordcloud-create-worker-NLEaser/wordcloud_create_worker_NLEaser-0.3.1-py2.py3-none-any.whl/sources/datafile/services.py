from typing import List
from werkzeug.datastructures import FileStorage

from models.datafile import DataFileSchema, DataFileModel
from models.user import UserModel

from sources.datafile.util import open_file
from sources.datafile.exceptions import TextColumnNotFound


def import_data_file(
        user: UserModel, file: FileStorage, format: str,
        text_column: str, language: str, separador=";") -> DataFileModel:

    datafile_schema = DataFileSchema()
    df = open_file(file, format, separador)

    if format != 'txt':
        if not text_column in df.columns:
            raise TextColumnNotFound("Não foi possivel encontrar a coluna " + text_column + " no conjunto de dados")

    data_file: DataFileModel = datafile_schema.load(
        {
            'name': file.filename,
            'format': format,
            'language': language,
            'text_column': text_column
        }
    )
    data_file.owner = user
    data_file.save()

    return {
        "df": df,
        "datafile": data_file
    }


def list_all_user_datafiles(user: UserModel ,orderby: str = "name", order_ascending: bool = True) -> List[DataFileModel]:
    documents = DataFileModel.objects(
        owner=user, excluded=False
    ).order_by(
        ("+" if order_ascending else "-") + orderby
    ).all()
    return documents


def get_datafile(user: UserModel, datafile_id: str) -> DataFileModel:
    datafile: DataFileModel = DataFileModel.objects(id=datafile_id, owner=user).first()
    if datafile is None:
        raise FileNotFoundError("Não foi encontrado nenhum arquivo com o id informado")
    return datafile


def delete_data_file(user: UserModel, datafile_id: str):
    datafile = get_datafile(user, datafile_id)
    datafile.excluded = True
    datafile.save()

    return datafile.excluded
