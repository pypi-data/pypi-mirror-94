from flask_jwt_extended import get_current_user
from pandas import DataFrame

from models.datafile import DataFileModel
from models.tasks.datafile.upload import DataFileUploadTaskModel
from sources.sentences.services import import_sentences_from_df, list_sentences_from_datafile, \
    delete_sentences_from_datafile
from sources.tasks.sentences.save import SentenceSaveTaskService


class SentencesService:
    def __init__(self, datafile: DataFileModel):
        self.user = get_current_user()
        self.datafile = datafile

    def import_sentences_from_df(self, df: DataFrame, datafile_import_task: DataFileUploadTaskModel):
        sentences_import_task_service = SentenceSaveTaskService(self.user)
        sentences_import_task_service.create(df, self.datafile, datafile_import_task)

    def list_sentences_from_datafile(self, skip: int, limit: int):
        return list_sentences_from_datafile(self.datafile, skip, limit)

    def delete_sentences_from_datafile(self):
        return delete_sentences_from_datafile(self.datafile)
