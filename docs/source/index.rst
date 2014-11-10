Django Perseus
==============

Builds a static version of your Django website.

Why would I need this?
======================

Let's say your webhost can only serve static files, then this package can statically generate
your Django website and you can upload the result to your webhost.

Downsides
=========

On a static website some restrictions apply:

- No conditions in template. ``{% if %}`` ``{% else %}`` blocks will not be very effective.
- No user input. No forms or dynamic pages.


Credits
=======

This project is based on the Django Medusa app which allows to render a Django website statically
Thanks Mike Tigas for your work :)

- `Django Medusa on Github <https://github.com/mtigas/django-medusa>`_

Contents
========

.. toctree::
   :maxdepth: 2

   installation
   usage



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

