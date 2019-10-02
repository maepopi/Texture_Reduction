set ffmpegpath=%~dp0..\..\ffmpeg\bin\ffmpeg.exe

set inputPath=%1

set inputFolder=%~dp0..\Input\Reduce_Only

set image_extension=%~x1


set image_name=%~n1

set resolution=2048

IF %image_extension% EQU .png (GOTO:png)
IF %image_extension% EQU .jpg (GOTO:jpg)
IF %image_extension% EQU .jpeg (GOTO:jpeg)

:png
set image_extension=png
goto:done

:jpg
set image_extension=jpg
goto:done

:jpeg
set image_extension=jpeg
goto:done

:done
echo image_extension is %image_extension%


REM use the instruction which keeps the image ratio, because some textures won't be square
"%ffmpegpath%" -i %1 -vf scale=%resolution%:-1 %image_name%_reduced.%image_extension%

set newimage_path=%1\..\%image_name%_reduced.%image_extension%

echo new image path is %newimage_path%

REM rename original in _old
ren "%1" "%image_name%_old.%image_extension%"

REM rename reduced in original (weird bug, you need to refresh the page for the final name to appear)
ren "%newimage_path%" "%image_name%.%image_extension%"




pause