import base64
import json
import logging
from io import BytesIO
from typing import List

from models.sentence import SentenceModel
from models.tasks.wordcloud.create import WordcloudCreateTaskModel
from models.wordcloud import WordcloudModel, WordcloudSchema

from sources.logger import create_logger
from sources.nlp.tfidf.wordcloud import generate_wordcloud

logger = logging.getLogger("wordcloud_create")


def create_base64_wordcloud(sentences: List[SentenceModel], language: str) -> bytes:
    pre_processed_sentences = [sentence.pre_processed_content for sentence in sentences]
    wordcloud = generate_wordcloud(pre_processed_sentences, language)
    image = wordcloud.to_image()
    buffer = BytesIO()
    image.save(buffer, "JPEG")
    image_base64 = base64.b64encode(buffer.getvalue())
    return image_base64


def process_task(wordcloud_create_task: WordcloudCreateTaskModel) -> bool:
    # Recupera as sentenças
    wordcloud_create_task.status = "in_progress"
    wordcloud_create_task.save()
    try:
        sentences: List[SentenceModel] = SentenceModel.objects(
            datafile=wordcloud_create_task.datafile,
            excluded=False
        ).all()
    except Exception as e:
        wordcloud_create_task.status = "error"
        wordcloud_create_task.error = "Erro ao importar as sentençs desse arquivo"
        wordcloud_create_task.save()
        logger.error(
            wordcloud_create_task.error,
            exc_info=True,
            extra={"received_args": wordcloud_create_task.to_mongo()}
        )
        return False

    # gera o wc em base64

    try:
        base64_image = create_base64_wordcloud(
            sentences,
            wordcloud_create_task.datafile.language
        )
    except Exception as e:
        wordcloud_create_task.status = "error"
        wordcloud_create_task.error = "Erro ao gerar o wordcloud em base64"
        wordcloud_create_task.save()
        logger.error(
            wordcloud_create_task.error,
            exc_info=True,
            extra={"received_args": wordcloud_create_task.to_mongo()}
        )
        return False

    # Salva o wc

    try:
        schema = WordcloudSchema()
        model: WordcloudModel = schema.load({
            "datafile": wordcloud_create_task.datafile,
            "base64_image": base64_image
        })
        model.save()
    except Exception as e:
        wordcloud_create_task.status = "error"
        wordcloud_create_task.error = "Erro ao salvar o wordcloud no bd"
        wordcloud_create_task.save()
        logger.error(
            wordcloud_create_task.error,
            exc_info=True,
            extra={"received_args": wordcloud_create_task.to_mongo()}
        )
        return False

    wordcloud_create_task.progress = 1
    wordcloud_create_task.status = "success"
    wordcloud_create_task.save()

    return True


def wordcloud_create_consumer(ch, method, properties, body):
    logger.debug("Recebido: " + body.decode(), extra={"received_args": body})

    try:
        task_info = json.loads(body.decode())
        logger.debug("Recuperando tarefa: " + task_info["task"])
        wordcloud_create_task: WordcloudCreateTaskModel = \
            WordcloudCreateTaskModel.objects(id=task_info["task"]).first()
        if wordcloud_create_task is None:
            raise Exception("Não foi encontrada nenhuma tarefa com o id " + task_info["task"])
    except Exception as e:
        logger.error(
            "Erro ao recuperar a tarefa",
            exc_info=True,
            extra={"received_args": body}
        )
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return False

    success_task = process_task(wordcloud_create_task)

    if success_task:
        ch.basic_ack(delivery_tag=method.delivery_tag)

    else:
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )

    return True
