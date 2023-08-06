import os

# CONFIGS FLASK
DEBUG = True
SECRET_KEY = "8eecf942-0f42-11eb-adc1-0242ac120002"
ENV = "development"
HOST = "localhost"
PORT = 5000

# CONFIGS DB
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "nleaser"

# CONFIGS JWT
JWT_SECRET_KEY = SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = 43200    # 12horas


# CONFIGS RABBIT
RABBIT_HOST = "host.docker.internal" if os.getenv("HOST") == "docker" else "localhost"
RABBIT_PORT = 5672
RABBIT_USER = "guest"
RABBIT_PASS = "guest"

RABBIT_QUEUES = {
    "NLEaser.sentence_import": {
        "exchange": "NLEaser",
        "queue": "sentence_import",
        "routing_key": "NLEaser.sentence_import"
    },
    "NLEaser.wordcloud_create": {
        "exchange": "NLEaser",
        "queue": "wordcloud_create",
        "routing_key": "NLEaser.wordcloud_create"
    }
}
