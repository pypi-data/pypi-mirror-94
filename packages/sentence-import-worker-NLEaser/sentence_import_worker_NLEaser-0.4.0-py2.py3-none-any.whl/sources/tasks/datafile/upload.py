from models.tasks.datafile.upload import DataFileUploadTaskModel, DataFileUploadTaskSchema
from models.user import UserModel


class DataFileUploadTaskService:
    def __init__(self, user: UserModel, imported_datafile: dict):
        self.user = user
        self.imported_datafile = imported_datafile
        self.datafile_import_schema = DataFileUploadTaskSchema()

    def create(self):
        datafile_import_task: DataFileUploadTaskModel = self.datafile_import_schema.load({
            "owner": str(self.user.id),
            "total": self.imported_datafile["df"].shape[1],
            "datafile": str(self.imported_datafile["datafile"].id)
        })
        datafile_import_task.save()
        return datafile_import_task
