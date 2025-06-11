import os

import environ

env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

print(os.path.join(BASE_DIR, '.env'))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
