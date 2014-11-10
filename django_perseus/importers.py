import logging
import os
import shutil
import zipfile

from django.conf import settings


logger = logging.getLogger('django_perseus')


def zip_dir(source_dir, file_name):
    store_path = getattr(settings, 'PERSEUS_BUILD_DIR', None)
    if not store_path:
        raise Exception('PERSEUS_BUILD_DIR not defined in settings.')

    if not os.path.isdir(store_path):
        os.makedirs(store_path)

    rel_path = os.path.abspath(os.path.join(source_dir, os.pardir))

    file_path = os.path.abspath(os.path.join(store_path, file_name))
    zip_file = zipfile.ZipFile(file_path, 'w')
    for root, dirs, files in os.walk(source_dir):
        for _file in files:
            location = os.path.join(root, _file)
            # path for file in zip archive
            zip_name = os.path.join(os.path.relpath(root, rel_path), _file)
            zip_file.write(location, arcname=zip_name)
            logger.debug('File: {0} added to {1}'.format(zip_name, file_name))
    zip_file.close()


class BaseImporter(object):
    '''
    Imports a selection of (sub) directories and copy them to the specified target directory
    with all its contents.
    '''

    target_dir = ''
    sub_dirs = []
    source_dir = ''
    ignores = ['.DS_Store', ]

    def __init__(self):
        self.target_dir = getattr(settings, self.target_dir, None)
        try:
            if not os.path.isdir(self.target_dir):
                os.makedirs(self.target_dir)
        except TypeError:
            raise Exception('Specify target dir')

        self.source_dir = getattr(settings, self.source_dir, None)
        if not self.source_dir:
            raise Exception('{} could not be found in settings as source_dir')

        if not os.path.isdir(self.source_dir):
            raise Exception(
                'Could not find the source_dir: {0}'.format(self.source_dir))

        self.import_folders()

    def import_folders(self):
        for path in self.sub_dirs:
            if path is None:
                continue

            # Copy all the directory contents to the target directory and ignore all other paterns
            elif path == '*':
                self.copy_directory(self.source_dir, self.target_dir)
                break

            # This should not be allowed
            elif path == '/' and len(path) > 1:
                raise Exception('Specify path. Found: /')

            # Handle directories
            else:
                origin_path = os.path.abspath(os.path.join(self.source_dir, path))
                dest_path = os.path.abspath(os.path.join(self.target_dir, path))

                # If directory found, copy contents
                if os.path.isdir(origin_path):
                    self.copy_directory(origin_path, dest_path)

                # If file found, copy file over
                if os.path.isfile(origin_path):
                    self.copy_file(origin_path, dest_path)

    def create_directory(self, directory):
        ''' Creates directory if it does not exist '''
        if not os.path.isdir(directory):
            os.makedirs(directory)
            logger.debug('Created directory: {0}'.format(directory))

    def copy_file(self, origin_file, destination_file):
        ''' Creates directory for file and copies file to new directory '''

        # create directory if not exists minus file
        self.create_directory('/'.join(destination_file.split('/')[:-1]))
        shutil.copy2(origin_file, destination_file)
        shutil.copystat(origin_file, destination_file)
        logger.debug('Copied: {0} to {1}'.format(origin_file, destination_file))

    def copy_directory(self, origin, destination):
        ''' Copies directories and files and recreates them recursively '''
        self.create_directory(destination)

        logger.debug('Copying contents of: {0} to {1}'.format(origin, destination))
        contents = os.listdir(origin)
        for obj in contents:
            if obj in self.ignores:
                logger.debug('Ignoring {0}/{1}'.format(origin, obj))
            else:
                original_path = os.path.abspath(os.path.join(origin, obj))
                new_path = os.path.abspath(os.path.join(destination, obj))
                if os.path.isfile(original_path):
                    self.copy_file(original_path, new_path)

                if os.path.isdir(original_path):
                    logger.debug('Found directory! Stepping in: {0}'.format(original_path))
                    self.copy_directory(original_path, new_path)
