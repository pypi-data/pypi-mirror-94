from typing import List

from flask_jwt_extended import get_current_user

from models.datafile import DataFileModel
from sources.datafile.services import delete_data_file, get_datafile, import_data_file, list_all_user_datafiles
from sources.sentences import SentencesService
from sources.tasks.datafile.upload import DataFileUploadTaskService


class DataFileService:
    def __init__(self):
        self.user = get_current_user()

    def import_datafile(self, file, format: str, text_column: str, language: str, separador=";") -> DataFileModel:
        imported_datafile = import_data_file(self.user, file, format, text_column,
                                             language, separador)

        datafile_import_task_service = DataFileUploadTaskService(
            self.user, imported_datafile
        )
        datafile_import_task = datafile_import_task_service.create()

        sentence_service = SentencesService(imported_datafile["datafile"])

        sentence_service.import_sentences_from_df(
            imported_datafile["df"],
            datafile_import_task
        )

        return imported_datafile["datafile"]

    def list_all_datafiles(self, orderby: str = "name", order_ascending: bool = True) -> List[DataFileModel]:
        documents = list_all_user_datafiles(self.user, orderby, order_ascending)
        return documents

    def get_datafile(self, datafile_id: str) -> DataFileModel:
        return get_datafile(self.user, datafile_id)

    def delete_datafile(self, datafile_id: str) -> bool:
        deleted = delete_data_file(self.user, datafile_id)
        if deleted:
            sentences_service = SentencesService(self.get_datafile(datafile_id))
            return sentences_service.delete_sentences_from_datafile()
        return deleted

    def get_sentences(self, datafile_id: str, skip: int, limit: int):
        datafile = self.get_datafile(datafile_id)
        sentences_service = SentencesService(datafile)
        return sentences_service.list_sentences_from_datafile(skip, limit)
