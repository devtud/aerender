# aerender

## Render Adobe After Effects projects using Python

**aerender** is an asyncio wrapper over `aerender` (Adobe After Effects 2019)
built and tested on Windows 10. It can be used to automate the rendering of
After Effects projects.

## Install it

    pip install aerender

## Usage example

- To render just Comp 1 to a specified file:

```python
import asyncio

from aerender import AERenderWrapper

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

if __name__ == '__main__':
    AERENDER_FULLPATH = 'C:\Program Files\Adobe\Adobe After Effects CC 2019\Support Files\\aerender'
    aerender = AERenderWrapper(exe_path=AERENDER_FULLPATH)
    coro = aerender.run(
        project_path='"c:\projects\proj1.aep"',
        comp_name='"Comp 1"',
        output_path='"c:\output\proj1\proj1.avi"',
    )
    asyncio.run(coro)
```

## `aerender -help`

Below you can see the `-help` output of `aerender` executable on Windows.

USAGE:
   1. `aerender` renders After Effects comps. The render may be performed either
      by an already running instance of AE or by a newly invoked instance. By
      default, `aerender` will invoke a new instance of AE, even if one is
      already running. To change this, see the `-reuse` flag below.

   2. `aerender` takes a series of optional arguments.

      Some are single flags, like `-reuse`. Some come in flag-argument
      pairs, like `-project project_path`. And one comes in a triplet,
      `-mem_usage image_cache_percent max_mem_percent`.

   3. `aerender` with 0 arguments, or with any argument equaling `-help`
      or `-h`, prints this usage message.

   4. The arguments are:

      - **`-h`**              print this usage message

      - **`-help`**           print this usage message

      - **`-reuse`**          use this flag if you want to try and reuse
                              an already running instance of AE to perform the
                              render.  By default, aerender will launch a new
                              instance of After Effects, even if one is already
                              running.  But, if AE is already running, and the
                              `-reuse` flag is provided, then `aerender` will
                              ask the already running instance of AE to perform
                              the render. Whenever `aerender` launches a new
                              instance of AE, it will tell AE to quit when
                              rendering is completed; otherwise, it will not
                              quit AE. Also, the preferences will be written
                              to file upon quit when the `-reuse` flag is
                              specified; otherwise it will not be written.

      - **`-project project_path`**
                            where **`project_path`** is a file path or URI
                            specifying a project file to open.
                            If none is provided, aerender will work with the
                            currently open project.
                            If no project is open and no project is provided,
                            an error will result.

      - **`-teamproject project_name`**
                            where **`project_name`** is a name of a
                            team project to open.

      - **`-comp comp_name`**
                            where **`comp_name`** specifies a comp to be rendered.
                            If the comp is in the render queue already, and
                            in a queueable state, then (only) the first
                            queueable instance of that comp on the render
                            queue will be rendered. If the comp is in the
                            project but not in the render queue, then it will
                            be added to the render queue and rendered.
                            If no `-comp` argument is provided, `aerender` will
                            render the entire render queue as is. In this
                            case (no `-comp`), the only other arguments used
                            will be `-project`, `-log`, `-v`, `-mem_usage`, and
                            `-close`; the `-RStemplate`, `-OMtemplate`, `-output`,
                            `-s`, `-e`,  and `-i` arguments will be ignored.

      - **`-rqindex index_in_render_queue`**
                            where **`index_in_render_queue`** specifies a
                            render queue item to be rendered. Options that make
                            sense when rendering a single render queue item
                            are available like with the `-comp` flag.

      - **`-RStemplate  render_settings_template`**
                            where **`render_settings_template`**
                            is the name of a template to apply to the render
                            queue item.If the template does not exist it is
                            an error.
                            Default is to use the render template already
                            defined for the item.

      - **`-OMtemplate  output_module_template`**
                            where **`output_module_template`**
                            is the name of a template to apply to the
                            output module. If the template does not exist
                            it is an error.
                            Default is to use the template already defined
                            for the output module.

      - **`-output  output_path`**
                            where **`output_path`** is a file path or URI
                            specifying the destination render file.
                            Default is the path already in the project file.

      - **`-log logfile_path`**
                            where **`logfile_path`** is a file path or URI
                            specifying the location of the log file.
                            Default is stdout.

      - **`-s start_frame`**
                            where **`start_frame`** is the first frame to render.
                            Default is the start frame in the file.

      - **`-e end_frame`**
                            where **`end_frame`** is the last frame to render.
                            Note, this is "inclusive;" the final frame
                            will be rendered.
                            Default is the end frame in the file.

      - **`-i increment`**
                            where **`increment`** is the number of frames to
                            advance before rendering a new frame. A value
                            of 1 (the default) results in a normal rendering
                            of all frames. Higher increments will repeat the
                            same (frame increment-1) times and then render a
                            new one, starting the cycle again. Higher values
                            result in faster renders but choppier motion.
                            Default is 1.

      - **`-mem_usage image_cache_percent max_mem_percent`**
                            where **`image_cache_percent`** specifies the maximum
                            percent of memory used to cache already rendered
                            images/footage, and **`max_mem_percent`** specifies
                            the total percent of memory that can be
                            used by After Effects.

      - **`-v verbose_flag`**
                            where **`verbose_flag`** specifies the type of
                            messages reported.  Possible values are `ERRORS`
                            (prints only fatal and problem errors) or
                            `ERRORS_AND_PROGRESS` (prints progress of rendering
                            as well).
                            Default value is `ERRORS_AND_PROGRESS`.

      - **`-close close_flag`**
                            where **`close_flag`** specifies whether or not to
                            close the project when done rendering, and
                            whether or not to save changes. If close_flag is
                            `DO_NOT_SAVE_CHANGES`, project will be closed
                            without saving changes. If close_flag is
                            `SAVE_CHANGES`, project will be closed and changes
                            will be saved. If close_flag is `DO_NOT_CLOSE` the
                            project will be left open; but the project is
                            left open only if using an already-running
                            instance of AE, since new invocations of AE must
                            always close and quit when done.
                            Default value is `DO_NOT_SAVE_CHANGES`.

      - **`-sound sound_flag`**
                            where **`sound_flag`** specifies whether or not to play
                            a sound when rendering is complete. Possible
                            values are "`ON`" or "`OFF`".
                            Default value is "`OFF`".

      - **`-version`**
                            displays the version number of aerender to the
                            console. Does not render.

      - **`-continueOnMissingFootage`**
                            Do not stop rendering on missing footage. Log and
                            render with placeholder color bars.

   5. EXAMPLES:
      To render just Comp 1 to a specified file:

          aerender -project c:\projects\proj1.aep -comp "Comp 1"
                   -output c:\output\proj1\proj1.avi

      To render everything in the render queue as is in the project file:

          aerender -project c:\projects\proj1.aep

      To render frames 1-10 using multi-machine render:

          aerender -project c:\projects\proj1.aep -comp "Comp 1" -s 1 -e 10
                   -RStemplate "Multi-Machine Settings"
                   -OMtemplate "Multi-Machine Sequence"
                   -output c:\output\proj1\frames[####].psd
