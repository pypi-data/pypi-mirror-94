import sys, os
import logging
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, DynamicField, IntField


class DBLogModel(Document):
    '''
    Grava exceções de erros na collection logs

    Parameters:
        args (str) : Argumentos da requisição
        stack (str) : Stack trace do erro
        error (str) : Exception string do erro

    '''
    meta = {
        'collection': 'log'
    }
    emiter = StringField(required=True)
    args = DynamicField(required=True)
    message = StringField()
    stack = StringField(default='')
    exceptionType = StringField(default='')
    exceptionDetails = DynamicField(default={})
    level = StringField()
    timestamp = DateTimeField(default=datetime.now)

    def save(self):
        """
            Salva o objeto no banco de dados,
            tambem realiza a extração do stack e do error caso a stack e o error estejam
            vazios
        """

        import traceback
        error_type, error_descryption, tb = sys.exc_info()
        self.stack = str(traceback.extract_tb(tb))
        self.exceptionType = str(error_type)

        try:
            self.exceptionDetails = vars(error_descryption)
            super().save()
        except Exception:
            self.exceptionDetails = str(self.exceptionDetails)


class DBLogHandler(logging.Handler):
    def __init__(self, level):
        return super().__init__(level)

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)

        log = DBLogModel(
            emiter=record.name,
            args=record.received_args if 'received_args' in record.__dict__.keys() else '',
            message=msg,
            level=record.levelname
        )
        log.save()


def create_logger(module_name, log_level=logging.DEBUG):
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    dbHandler = DBLogHandler(log_level)
    logger.addHandler(dbHandler)

    if os.getenv('ENV') == 'development':
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

    return logger
