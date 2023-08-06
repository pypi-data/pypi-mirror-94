import json
import logging

from mongoengine import NotUniqueError
from pika.channel import Channel

from models.tasks.datafile.upload import DataFileUploadTaskModel
from models.tasks.sentence.save import SentenceSaveTaskModel
from models.sentence import SentenceModel, SentenceSchema

from sources.logger import create_logger
from sources.nlp.preprocessing import tokenize, remove_token_accents, mask_token_numbers

logger = logging.getLogger("sentence_import")


def preprocess_sentence(sentence: str, language: str) -> str:
    p_sentence = sentence.lower()

    tokens = tokenize(p_sentence, language)
    tokens = map(remove_token_accents, tokens)
    tokens = map(mask_token_numbers, tokens)

    p_sentence = " ".join(tokens)

    return p_sentence


def process_task(sentences_import_task: SentenceSaveTaskModel) -> bool:
    # preprocessa a sentença
    try:
        preprocessed_sentence = preprocess_sentence(sentences_import_task.content,
                                                    sentences_import_task.datafile.language)

    except Exception as e:
        sentences_import_task.status = "error"
        sentences_import_task.error = "Erro ao preprocessar a sentenca"
        sentences_import_task.save()
        logger.error(
            "Erro ao preprocessar a sentenca",
            exc_info=True,
            extra={"received_args": sentences_import_task.to_mongo()})
        return False

    # salva a sentença

    try:
        schema = SentenceSchema()
        sentence: SentenceModel = schema.load({
            "datafile": sentences_import_task.datafile,
            "index": sentences_import_task.index,
            "content": sentences_import_task.content,
            "pre_processed_content": preprocessed_sentence
        })
        sentence.save()
    except NotUniqueError:
        pass

    except Exception as e:
        sentences_import_task.status = "error"
        sentences_import_task.error = "Erro ao salvar a sentença"
        sentences_import_task.save()
        logger.error(
            "Erro ao salvar a sentença",
            exc_info=True,
            extra={"received_args": sentences_import_task.to_mongo()})
        return False

    # Atualiza o status da tarefa
    sentences_import_task.progress = 1
    sentences_import_task.status = "success"
    sentences_import_task.save()

    return True


def sentence_preprocessor_consumer(ch: Channel, method, properties, body):
    logger.debug("Recebido: " + body.decode(), extra={"received_args": body})

    # Recupera as informações da tarefa
    try:
        task_info = json.loads(body.decode())
        logger.debug("Recuperando tarefa: " + task_info["task"])
        sentences_import_task: SentenceSaveTaskModel = SentenceSaveTaskModel.objects(id=task_info["task"]).first()
        if sentences_import_task is None:
            raise Exception("Não foi encontrada nenhuma tarefa com o id " + task_info["task"])

    except Exception as e:
        logger.error("Erro ao recuperar a tarefa", exc_info=True, extra={"received_args": body})
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return False

    success_task = process_task(sentences_import_task)

    datafile_import_task = sentences_import_task.parent

    DataFileUploadTaskModel.objects(
        id=datafile_import_task.id,
        progress__lt=datafile_import_task.total
    ).update_one(inc__progress=1)

    if success_task:
        ch.basic_ack(delivery_tag=method.delivery_tag)

    else:
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )

    datafile_import_task.reload("progress", "total")
    if datafile_import_task.progress >= datafile_import_task.total:
        tasks_with_fail = SentenceSaveTaskModel.objects(
            parent=datafile_import_task,
            status="error"
        ).count()

        logger.debug("Tarefa de importação concluida: " + str(datafile_import_task.id))

        if tasks_with_fail > 0:
            datafile_import_task.status = "error"
            datafile_import_task.error = "Algumas das sentenças não foram importadas com sucesso"
        else:
            datafile_import_task.status = "success"

        datafile_import_task.save()

    logger.debug("Tarefa concluida: " + task_info["task"])

    return True

