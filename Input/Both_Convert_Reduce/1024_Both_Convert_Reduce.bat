set ffmpegpath=%~dp0..\ffmpeg\bin\ffmpeg.exe

set inputPath=%1

set inputFolder=%~dp0..\Input


set image_name=%~n1

set image_extension=%~x1



set resolution=1024

IF %image_extension% EQU .tga (GOTO:tga) 
IF %image_extension% EQU .bmp (GOTO:bmp) 
IF %image_extension% EQU .png (GOTO:png) 
IF %image_extension% EQU .jpg (GOTO:jpg) 
IF %image_extension% EQU .jpeg (GOTO:jpeg) 
IF %image_extension% EQU .tiff (GOTO:tiff) 
IF %image_extension% EQU .gif (GOTO:gif) 


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


"%ffmpegpath%" -i %1 -vf scale=%resolution%:-1 %image_name%_reduced_converted.png

set newimage_path=%1\..\%image_name%_reduced_converted.png

ren "%1" "%image_name%_old.%image_extension%"

ren "%newimage_path%" "%image_name%".png

pause



pause