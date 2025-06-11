import environ

env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
)
