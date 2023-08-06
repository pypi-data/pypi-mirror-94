from threading import Thread

from sources.sentences.services import import_sentences_from_df


class SentenceSaveTaskService:

    def __init__(self, user):
        self.user = user

    def create(self, df, datafile, datafile_import_task):
        import_sentences_thread = Thread(
            target=import_sentences_from_df,
            args=[df, datafile, datafile_import_task]
        )
        import_sentences_thread.start()
