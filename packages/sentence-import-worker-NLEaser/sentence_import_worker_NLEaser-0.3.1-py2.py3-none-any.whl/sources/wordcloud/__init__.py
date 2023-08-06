from flask_jwt_extended import get_current_user

from models.datafile import DataFileModel
from models.tasks.wordcloud.create import WordcloudCreateTaskModel
from models.wordcloud import WordcloudModel
from sources.wordcloud.services import delete_wordclouds_from_datafile, get_wordclouds_from_datafile
from sources.tasks.wordcloud.create import WordcloudCreateTaskService


class WordcloudService:
    def __init__(self, datafile_id: int = None):
        self.user = get_current_user()
        if datafile_id:
            self.datafile = DataFileModel.objects(
                owner=self.user, id=datafile_id, excluded=False
            ).first()

    def create_wordcloud(self) -> WordcloudCreateTaskModel:
        service = WordcloudCreateTaskService(self.user)
        create_wordcloud_task = service.create(self.datafile)
        return create_wordcloud_task

    def get_wordcloud(self) -> WordcloudModel:
        wcs = get_wordclouds_from_datafile(self.datafile)
        return wcs.first()

    def delete_wordcloud(self) -> bool:
        deleted = delete_wordclouds_from_datafile(self.datafile)
        return deleted
