import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'test'

DATABASES = {}

INSTALLED_APPS = (
    'django_perseus',
    'django_perseus.tests.testapp1',
    'django_perseus.tests.testapp2',
)

ROOT_URLCONF = 'django_perseus.tests.urls'

STATIC_URL = '/'
MEDIA_URL = '/'

PERSEUS_SOURCE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'django_perseus', 'tests', 'source'))
PERSEUS_BUILD_DIR = os.path.abspath(os.path.join(BASE_DIR, 'django_perseus', 'tests', 'build'))

TEST_STATIC = os.path.abspath(os.path.join(BASE_DIR, 'django_perseus', 'tests', 'static'))

PERSEUS_IMPORTERS = [
    'django_perseus.tests.testapp2.importers.TestImporter',
]
