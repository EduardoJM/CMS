import os

import environ

env = environ.Env(
    DEBUG=(bool, False),
    SITE_NAME=(str, "CMS"),
    SECRET_KEY=(str, 'insecure-secret-key'),
    USE_S3=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    BASE_URL=(str, ''),
)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
