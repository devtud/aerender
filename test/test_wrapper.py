import asyncio
from pathlib import Path
from unittest import TestCase

from aerender import AERenderWrapper


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
