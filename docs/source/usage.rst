Usage
=====

Django Perseus consists of few modules working together to sucessfully render a static html site.

- Template tags
    They overwrite Django's builtin url and static tags to rewrite them statically.

- Renderer
    Selects views and renders them as static pages.

- Importer
    Imports a selection of static and media files to the output directory of the renderer.


Renderer
--------

Django Perseus will look for renderers.py file in your Django apps.

You can subclass the ``BaseRenderer`` to create a custom renderer, or use the ``DefaultRenderer``
to render your Django website with the default behaviour.

.. code-block:: python

    from django_perseus.renderers.default import DefaultRenderer


    class AppRenderer(DefaultRenderer):

        def paths(self):
            return [
                reverse('index'),
                reverse('privacy'),
                reverse('app:index'),
                reverse('app:settings'),
                reverse('app:detail', kwargs={'pk': 1}),
                reverse('app:archive', kwargs={'year': 2014, 'week': 52}),
            ]


    renderers = [AppRenderer, ]


The output of the example will be:

.. code-block:: bash

    output_dir/index.html
    output_dir/privacy.html
    output_dir/app.html
    output_dir/app/settings.html
    output_dir/app/detail/1.html
    output_dir/app/archive/2014/52.html


Importer
--------

You can subclass ``BaseImporter`` to import files from specific locations in your Django app to a
target directory

Your static website will need a selection of media and static files.

The ``BaseImporter`` accepts the following class attributes:

- ``target_dir`` (Django setting) the target directory where the files will be copied to.
- ``source_dir`` (Django setting) the source directory where the files will be copied from.
- ``sub_dirs`` (List) subdirectories or files to be imported.


Example media files importer:

.. code-block:: python

    class MediaImporter(BaseImporter):

        target_dir = 'PERSEUS_SOURCE_DIR'
        source_dir = 'MEDIA_ROOT'
        sub_dirs = [
            '*'
        ]

Example static files importer:

.. code-block:: python

    class StaticImporter(BaseImporter):

        target_dir = 'PERSEUS_SOURCE_DIR'
        source_dir = 'STATIC_ROOT'
        sub_dirs = [
            'css',
            'img',
            'js/build',
            'robots.txt',
        ]


Register the importer subclass in your perseus settings file:

.. code-block:: python

    PERSEUS_IMPORTERS = [
        'yourproject.app.importers.MediaImporter',
        'yourproject.app.importers.StaticImporter',
    ]


Template tags
-------------

The tags rewrite paths when the ``render`` management command is run with a settings file
containing the setting: ``RENDER_STATIC = True``

Load the tags in your templates as:

.. code-block:: html

    {% load django_perseus_tags %}


Management command
------------------

The ``render`` management command will run all renderers found in your Django apps and run
the file importers.

::

    ./manage.py render --settings=yourproject.conf.perseus_settings.py

To also output the result in a zip archive, run as:

::

    ./manage.py render --archive --settings=yourproject.conf.perseus_settings.py

    ./manage.py render --archive --filename filename.zip --settings=yourproject.conf.perseus_settings.py


Settings
--------


- ``RENDER_STATIC``
    A boolean whether the url and static tags will be rewritten to static paths.

- ``PERSEUS_SOURCE_DIR``
    renderer output folder

- ``PERSEUS_BUILD_DIR``
    output dir if render management command runs with ``--archive`` option

- ``PERSEUS_IMPORTERS``
    A list where Importers are to be found.

.. code-block:: python

    PERSEUS_IMPORTERS = [
        'yourproject.app.importers.MediaImporter',
        'yourproject.app.importers.StaticImporter',
    ]
