from contextlib import nested
from mock import patch

from django_perseus.management.commands.render import Command


class TestRenderCommand:

    mock_paths = (
        patch('django_perseus.management.commands.render.run_renderers'),
        patch('django_perseus.management.commands.render.run_importers'),
        patch('django_perseus.management.commands.render.zip_dir'),
    )

    def test_command_default(self):
        with nested(*self.mock_paths) as (
            run_renderers_mock,
            run_importers_mock,
            zip_dir_mock,
        ):
            Command().handle()
            assert run_renderers_mock.called
            assert run_importers_mock.called
            assert not zip_dir_mock.called

    def test_command_archive_no_filename(self):
        with nested(*self.mock_paths) as (
            run_renderers_mock,
            run_importers_mock,
            zip_dir_mock,
        ):
            Command().handle(archive=True)
            assert run_renderers_mock.called
            assert run_importers_mock.called
            zip_dir_mock.assert_called_once_with('render.zip')

    def test_command_archive_with_filename(self):
        with nested(*self.mock_paths) as (
            run_renderers_mock,
            run_importers_mock,
            zip_dir_mock,
        ):
            Command().handle(archive=True, filename='custom.zip')
            assert run_renderers_mock.called
            assert run_importers_mock.called
            zip_dir_mock.assert_called_once_with('custom.zip')
