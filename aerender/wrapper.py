import asyncio
import logging
from asyncio import StreamReader
from pathlib import Path

from .exceptions import (AERenderError, AfterEffectsError, CompositionNotFoundError,
                         PathNotFoundError)


__all__ = ['AERenderWrapper']

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('aerender')


class AERenderWrapper:
    def __init__(self, exe_path: Path):
        self.exe_path: Path = exe_path

    async def run(
        self, reuse: bool = None, project_path: Path = None, project_name: str = None,
        comp_name: str = None, index_in_render_queue: str = None,
        render_settings_template: str = None, output_module_template: str = None,
        output_path: Path = None, logfile_path: Path = None, start_frame: int = None,
        end_frame: int = None, increment: int = None, image_cache_percent: int = None,
        max_mem_percent: int = None, verbose_flag: str = None, close_flag: str = None,
        sound_flag: str = None, continue_on_missing_footage: bool = None,
        version: bool = None):
        """
        Args:
            reuse: use this flag if you want to try and reuse an already running instance
                of AE to perform the render. By default, aerender will launch a new
                instance of After Effects, even if one is already running. But, if AE is
                already running, and the -reuse flag is provided, then aerender will ask
                the already running instance of AE to perform the render. Whenever
                aerender launches a new instance of AE, it will tell AE to quit when
                rendering is completed; otherwise, it will not quit AE. Also, the
                preferences will be written to file upon quit when the -reuse flag is
                specified; otherwise it will not be written.
            project_path: a file path or URI specifying a project file to open. If none is
                provided, aerender will work with the currently open project. If no
                project is open and no project is provided, an error will result.
            project_name: a name of a team project to open
            comp_name: specifies a comp to be rendered. If the comp is in the render queue
                already, and in a queueable state, then (only) the first queueable
                instance of that comp on the render queue will be rendered. If the comp
                is in the project but not in the render queue, then it will be added to
                the render queue and rendered. If no -comp argument is provided,
                aerender will render the entire render queue as is. In this case
                (no -comp), the only other arguments used will be -project, -log, -v,
                -mem_usage, and -close; the -RStemplate, -OMtemplate, -output, -s,
                -e, and -i arguments will be ignored.
            index_in_render_queue: specifies a render queue item to be rendered. Options
                that make sense when rendering a single render queue item are available
                like with the -comp flag.
            render_settings_template: the name of a template to apply to the render
                queue item.If the template does not exist it is an error. Default is to
                use the render template already defined for the item
            output_module_template: the name of a template to apply to the output module.
                If the template does not exist it is an error. Default is to use the
                template already defined for the output module
            output_path: is a file path or URI specifying the destination render file.
                Default is the path already in the project file
            logfile_path: is a file path or URI specifying the location of the log file.
                Default is stdout
            start_frame: the first frame to render. Default is the start frame in the file
            end_frame: the last frame to render. Note, this is "inclusive;" the final
                frame will be rendered. Default is the end frame in the file
            increment: the number of frames to advance before rendering a new frame. A
                value of 1 (the default) results in a normal rendering of all frames.
                Higher increments will repeat the same (frame increment-1) times and then
                render a new one, starting the cycle again. Higher values result in
                faster renders but choppier motion. Default is 1
            image_cache_percent: specifies the maximum percent of memory used to cache
                already rendered images/footage
            max_mem_percent: specifies the total percent of memory that can be used
                by After Effects
            verbose_flag: specifies the type of messages reported. Possible values are
                ERRORS (prints only fatal and problem errors) or
                ERRORS_AND_PROGRESS (prints progress of rendering as well).
                Default value is ERRORS_AND_PROGRESS
            close_flag: specifies whether or not to close the project when done rendering,
                and whether or not to save changes. If close_flag is
                DO_NOT_SAVE_CHANGES, project will be closed without saving changes. If
                close_flag is SAVE_CHANGES, project will be closed and changes will
                be saved. If close_flag is DO_NOT_CLOSE the project will be left open;
                but the project is left open only if using an already-running instance
                of AE, since new invocations of AE must always close and quit when done.
                Default value is DO_NOT_SAVE_CHANGES
            sound_flag: specifies whether or not to play a sound when rendering is
                complete. Possible values are "ON" or "OFF". Default value is "OFF"
            continue_on_missing_footage: Do not stop rendering on missing footage. Log and
                render with placeholder color bars.
            version: displays the version number of aerender to the console. Does not
                render

        Returns:

        """
        command = await self.get_command(
            aerender_abs_path=self.exe_path, reuse=reuse, project_path=project_path,
            project_name=project_name, comp_name=comp_name,
            index_in_render_queue=index_in_render_queue,
            render_settings_template=render_settings_template,
            output_module_template=output_module_template, output_path=output_path,
            logfile_path=logfile_path, start_frame=start_frame, end_frame=end_frame,
            increment=increment, image_cache_percent=image_cache_percent,
            max_mem_percent=max_mem_percent, verbose_flag=verbose_flag,
            close_flag=close_flag, sound_flag=sound_flag,
            continue_on_missing_footage=continue_on_missing_footage, version=version)
        result = await self.run_command(command)
        return result

    @staticmethod
    async def run_command(command: str):
        async def log_generator(reader: StreamReader, tag: str):
            while True:
                line = await reader.readline()
                if not line:
                    break
                decoded = line.decode().strip()
                yield decoded, tag

        async def check_and_raise(log_line: str):
            if 'After Effects error' in log_line:
                if 'Path is not valid' in log_line:
                    raise PathNotFoundError(log_line)
                raise AfterEffectsError(log_line)
            if 'aerender ERROR' in log_line:
                if 'No comp was found with the given name' in log_line:
                    raise CompositionNotFoundError(log_line)
                raise AERenderError(log_line)
            if 'LoadLibrary "n" failed' in log_line:
                raise AERenderError(log_line)

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        process_task = asyncio.create_task(process.wait())

        stdout_log_generator = log_generator(process.stdout, 'stdout')

        # TODO check and parse stderr also
        # stderr_log_generator = log_generator(process.stderr, 'stderr')

        async for log_line, log_tag in stdout_log_generator:
            logger.info(f'{log_tag}: {log_line}')
            try:
                await check_and_raise(log_line)
            except AERenderError as e:
                logger.error(f'Waiting for process to finish due to error: {e}')
                await process_task
                raise e

        await asyncio.gather(process_task)

        logger.info(f'[{command!r} exited with {process.returncode}]')

        return None

    @staticmethod
    async def get_command(
        aerender_abs_path: Path, *, reuse: bool = None, project_path: Path = None,
        project_name: str = None, comp_name: str = None,
        index_in_render_queue: str = None, render_settings_template: str = None,
        output_module_template: str = None, output_path: Path = None,
        logfile_path: Path = None, start_frame: int = None, end_frame: int = None,
        increment: int = None, image_cache_percent: int = None,
        max_mem_percent: int = None, verbose_flag: str = None, close_flag: str = None,
        sound_flag: str = None, continue_on_missing_footage: bool = None,
        version: bool = None
    ) -> str:

        command = f'"{aerender_abs_path}"'
        if reuse:
            command += f' -reuse'
        if project_path is not None:
            command += f' -project "{project_path}"'
        if project_name is not None:
            command += f' -teamproject "{project_name}"'
        if comp_name is not None:
            command += f' -comp "{comp_name}"'
        if index_in_render_queue is not None:
            command += f' -rqindex {index_in_render_queue}'
        if render_settings_template is not None:
            command += f' -RStemplate "{render_settings_template}"'
        if output_module_template is not None:
            command += f' -OMtemplate "{output_module_template}"'
        if output_path is not None:
            command += f' -output "{output_path}"'
        if logfile_path is not None:
            command += f' -log "{logfile_path}"'
        if start_frame is not None:
            command += f' -s {start_frame}'
        if end_frame is not None:
            command += f' -e {end_frame}'
        if increment is not None:
            command += f' -i {increment}'
        if image_cache_percent is not None and max_mem_percent is not None:
            command += f' -mem_usage {image_cache_percent} {max_mem_percent}'
        if verbose_flag is not None:
            assert verbose_flag in ['ERRORS', 'ERRORS_AND_PROGRESS']
            command += f' -v {verbose_flag}'
        if close_flag is not None:
            assert close_flag in ['DO_NOT_SAVE_CHANGES', 'SAVE_CHANGES', 'DO_NOT_CLOSE']
            command += f' -close {close_flag}'
        if sound_flag is not None:
            assert sound_flag in ['ON', 'OFF']
            command += f' -sound {sound_flag}'
        if continue_on_missing_footage:
            command += f' -continueOnMissingFootage'
        if version:
            command += f' -version'
        return command
