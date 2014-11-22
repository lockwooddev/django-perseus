from django.conf import settings
from django.test.client import Client

from .base import BaseRenderer
from django_perseus.exceptions import RendererException

import logging
import mimetypes
import os


logger = logging.getLogger('perseus')


class DefaultRenderer(BaseRenderer):

    def render_path(self, path=None, view=None):
        if path:
            # create deploy dir if not exists
            deploy_dir = settings.PERSEUS_SOURCE_DIR
            outpath = os.path.join(deploy_dir, '')
            if not os.path.exists(deploy_dir):
                os.makedirs(deploy_dir)

            # create index page
            if path == '/':
                response, mime = self.render_page(path)
                outpath = os.path.join(outpath, 'index{0}'.format(mime))
                self.save_page(response, outpath)
                return

            # strip paths to ready them for mimetyping
            if path.startswith('/'):
                realpath = path[1:]
                if realpath.endswith('/'):
                    realpath = realpath[:-1]

            # split paths to find subdirs
            paths = path.split('/')
            paths = [p for p in paths if p != '']
            # if found more than one, subdirectories exist
            if len(paths) > 1:
                outdir = os.path.abspath(os.path.join(deploy_dir, *paths[:-1]))

                if not os.path.exists(outdir):
                    os.makedirs(outdir)

                response, mime = self.render_page(path)
                outpath = os.path.join(outdir, '{0}{1}'.format(paths[-1], mime))
                self.save_page(response, outpath)
            else:
                response, mime = self.render_page(path)
                outpath = os.path.join(outpath, '{0}{1}'.format(realpath, mime))
                self.save_page(response, outpath)

    def render_page(self, path):
        response = self.client.get(path)
        if response.status_code is not 200:
            raise RendererException(
                'Path: {0} returns status code: {1}.'.format(path, response.status_code))
        return response, self.get_mime(response)

    def get_mime(self, response):
        mime = response['Content-Type']
        encoding = mime.split(';', 1)[0]
        return mimetypes.guess_extension(encoding)

    def save_page(self, response, outpath):
        logger.debug(outpath)
        with open(outpath, 'wb') as f:
            f.write(response.content)

    def generate(self):
        self.client = Client()
        for path in self.paths():
            self.render_path(path=path)
