from mongoengine import QuerySet

from models.datafile import DataFileModel
from models.wordcloud import WordcloudModel


def get_wordclouds_from_datafile(datafile: DataFileModel) -> QuerySet:
    wcs = WordcloudModel.objects(
        datafile=datafile, excluded=False
    ).order_by("-created_at")
    return wcs


def delete_wordclouds_from_datafile(datafile: DataFileModel) -> bool:
    deleted = WordcloudModel.objects(
        datafile=datafile, excluded=False
    ).update(set__excluded=True)
    return deleted > 0
