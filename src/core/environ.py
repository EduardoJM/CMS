import environ

env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
)
