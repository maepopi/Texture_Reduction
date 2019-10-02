set ffmpegpath=%~dp0..\..\ffmpeg\bin\ffmpeg.exe

set inputPath=%1

set inputFolder=%~dp0..\Input\Convert_Only


set image_name=%~n1

if exist "%1.png" goto:png
if exist "%1.jpg" goto:jpg
if exist "%1.jpeg" goto:jpeg
if exist "%1.tga" goto:tga
if exist "%1.bmp" goto:bmp
if exist "%1.tiff" goto:tiff
if exist "%1.heic" goto:heic
if exist "%1.gif" goto:gif

:png
set image_extension=png
goto:done

:jpg
set image_extension=jpg
goto:done

:jpeg
set image_extension=jpeg
goto:done

:tga
set image_extension=tga
goto:done

:bmp
set image_extension=bmp
goto:done

:tiff
set image_extension=tiff
goto:done

:heic
set image_extension=jpeg
goto:done

:gif
set image_extension=gif
goto:done


:done
echo image_extension is %image_extension%


"%ffmpegpath%" -i %1 %image_name%.png



pause