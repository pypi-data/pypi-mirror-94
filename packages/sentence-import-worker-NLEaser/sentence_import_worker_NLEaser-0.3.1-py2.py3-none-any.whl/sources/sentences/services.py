import json
from typing import List, Union

from pandas import DataFrame

from models.datafile import DataFileModel
from models.sentence import SentenceModel
from models.tasks.datafile.upload import DataFileUploadTaskModel
from models.tasks.sentence.save import SentenceSaveTaskModel, SentenceSaveTaskSchema

from sources.logger import create_logger
from sources.rabbit.producer import RabbitProducer

logger = create_logger(__name__)


def import_sentences_from_df(df: DataFrame, datafile: DataFileModel,
                             datafile_import_task: DataFileUploadTaskModel) -> None:
    logger.info("Importando sentenças", extra={"received_args": {
        "datafile": datafile.id
    }})
    datafile_import_task.status = "in_progress"
    datafile_import_task.save()
    text_column = datafile.text_column
    try:

        schema = SentenceSaveTaskSchema()
        producer = RabbitProducer("NLEaser.sentence_import")
        for index, row in df.iterrows():
            sentence_import_task: SentenceSaveTaskModel = schema.load({
                "owner": str(datafile.owner.id),
                "datafile": str(datafile.id),
                "parent": str(datafile_import_task.id),
                "total": 1,
                "content": row[text_column],
                "index": index
            })
            sentence_import_task.save()
            producer.send_message(json.dumps({
                "task": str(sentence_import_task.id)
            }))
    except Exception as e:
        datafile_import_task.status = "error"
        datafile_import_task.error = "Erro desconhecido ao importar as sentenças"
        datafile_import_task.save()
        logger.error(
            "Erro ao importar sentenças do dataframe",
            exc_info=True,
            extra={"received_args": {
                "datafile": datafile.id,
                "upload": datafile_import_task.id,
                "text_column": text_column
            }}
        )


def list_sentences_from_datafile(datafile: DataFileModel, skip: int, limit: int) -> Union[List[SentenceSaveTaskModel], int]:
    sentences = SentenceModel.objects(
        datafile=datafile,
        excluded=False
    )
    total = sentences.count()
    sentences_pag = sentences.skip(skip).limit(limit)

    return sentences_pag, total


def delete_sentences_from_datafile(datafile: DataFileModel) -> bool:

    deleted = SentenceModel.objects(datafile=datafile).update(set__excluded=True)

    return deleted > 0
