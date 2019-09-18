import asyncio
import sys
from functools import partial
from pathlib import Path
from unittest import TestCase

from aerender import AERenderWrapper
from aerender.exceptions import PathNotFoundError, CompositionNotFoundError, AERenderError


if sys.platform == 'win32':
    print('Windows OS detected. Using asyncio.WindowsProactorEventLoopPolicy')
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


class TestWrapper(TestCase):
    def test_get_command(self):
        command = asyncio.run(AERenderWrapper.get_command(
            aerender_abs_path=Path(
                'C:/Program Files/Adobe/Adobe After Effects CC 2019/Support Files/aerender.exe'),
            project_path=Path('C:/Program Files/adobe/Desktop/project'),
            comp_name='Composition name',
            output_module_template='output template',
            output_path=Path('C:/Program Files/adobe/Desktop/movie.mov')
        ))
        expected = '"C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files\\aerender.exe" -project "C:\Program Files\\adobe\Desktop\project" -comp "Composition name" -OMtemplate "output template" -output "C:\Program Files\\adobe\Desktop\movie.mov"'
        self.assertEqual(expected, command)

    def test_run_command_must_raise_error_if_not_existing_composition(self):
        command = '"C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files\\aerender.exe" -comp "Composition name"'
        coro = AERenderWrapper.run_command(command)
        error_func = partial(asyncio.run, coro)
        self.assertRaises(CompositionNotFoundError, error_func)

    def test_run_command_must_raise_error_if_nothing_to_render(self):
        command = '"C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files\\aerender.exe" -OMtemplate "output template"'
        coro = AERenderWrapper.run_command(command)
        error_func = partial(asyncio.run, coro)
        self.assertRaises(AERenderError, error_func)

    def test_run_command_must_raise_error_if_not_existing_project_path(self):
        command = '"C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files\\aerender.exe" -project "C:\Program Files\\adobe\Desktop\project"'
        coro = AERenderWrapper.run_command(command)
        error_func = partial(asyncio.run, coro)
        self.assertRaises(PathNotFoundError, error_func)
