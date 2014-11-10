Installation
============

* Install Django Perseus::

    pip install django-perseus


* Add ``'django_perseus'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        "django_perseus",
    )

* Add Django Perseus settings to a separate settings file::

    from yourproject.settings_file import *

    # used by the template tags
    RENDER_STATIC = True

    # folder where the output is stored
    PERSEUS_SOURCE_DIR = ''

    # folder where the archive of the output is stored
    PERSEUS_BUILD_DIR = ''

    # where your importer classes are
    PERSEUS_IMPORTERS = [
        'yourproject.app.importers.MediaImporter',
        'yourproject.app.importers.StaticImporter',
    ]
