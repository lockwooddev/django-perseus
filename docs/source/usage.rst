Usage
=====

Renderer classes
----------------

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



File importer classes
---------------------

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

The custom template tags found in this package, overwrite the django builtin ``static`` and ``url`` tags. The tags rewrite paths when the ``render`` management command is run with a settings file
containing the setting: ``RENDER_STATIC = True``

Load the tags in your templates as:

.. code-block:: html

    {% load django_perseus_tags %}


Rendering
---------

The ``render`` management command will run all renderer classes found in your Django apps and run
the file importers.

::

    ./manage.py render --settings=yourproject.conf.perseus_settings.py

Output
------

In your ``PERSEUS_SOURCE_DIR`` your will find the following output for the example renderers found
found in this document.

Output of the ``paths`` method your renderer class with the corresponding url patterns

.. code-block:: python

    # ---------
    # root urls
    # ---------

    url(r'^$', SomeView.as_view(), name='index'),
    reverse('index')
    PERSEUS_SOURCE_DIR/index.html

    url(r'^privacy/$', SomeView.as_view(), name='privacy'),
    reverse('privacy')
    PERSEUS_SOURCE_DIR/privacy.html

    # --------
    # App urls
    # --------

    url(r'^$', SomeView.as_view(), name='index'),
    reverse('app:index')
    PERSEUS_SOURCE_DIR/app.html

    url(r'^settings/$', SomeView.as_view(), name='settings'),
    reverse('app:settings')
    PERSEUS_SOURCE_DIR/app/settings.html

    url(r'^detail/(?P<pk>[\d]+)/$', SomeView.as_view(), name='detail'),
    reverse('app:detail', kwargs={'pk': 1})
    PERSEUS_SOURCE_DIR/app/detail/1.html

    url(r'^archive/(?P<year>\d{4})/(?P<week>\d{2})$', SomeView.as_view(), name='archive'),
    reverse('app:archive', kwargs={'year': 2014, 'week': 52}),
    PERSEUS_SOURCE_DIR/app/archive/2014/52.html
