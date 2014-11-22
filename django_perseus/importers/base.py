from django.conf import settings

from django_perseus.exceptions import ImporterException

import logging
import os
import shutil


logger = logging.getLogger('django_perseus')


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
        # Check for attributes in settings
        self.target_dir = getattr(settings, self.target_dir, None)
        try:
            if not os.path.isdir(self.target_dir):
                os.makedirs(self.target_dir)
        except TypeError:
            raise ImporterException('target_dir cannot be found in your settings file.')

        self.source_dir = getattr(settings, self.source_dir, None)
        try:
            if not os.path.isdir(self.source_dir):
                raise ImporterException(
                    'No files can be imported, because source_dir does not exist.')
        except TypeError:
            raise ImporterException('source_dir cannot be found in your settings file.')

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
            elif path.startswith('/'):
                raise ImporterException('Absolute paths not allowed in sub_dirs')

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
