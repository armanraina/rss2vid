@echo off
@cd /d "%~dp0"
@set "ERRORLEVEL="
@CMD /C EXIT 0
@"%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" >nul 2>&1
@if NOT "%ERRORLEVEL%"=="0" (
@powershell -Command Start-Process ""%0"" -Verb runAs 2>nul
@exit
)
:--------------------------------------
@TITLE Mesa3D system-wide deployment utility
@echo Mesa3D system-wide deployment utility
@echo -------------------------------------
@echo This deployment utility targets systems without working GPUs and any use case
@echo where hardware accelerated OpenGL is not available. This mainly covers
@echo virtual machines in cloud environments and RDP connections. It can be
@echo used to replace Microsoft Windows inbox OpenGL 1.1 software render
@echo driver with Mesa3D softpipe, llvmpipe or swr driver.
@echo.
@set mesaloc=%~dp0
@IF "%mesaloc:~-1%"=="\" set mesaloc=%mesaloc:~0,-1%

:deploy
@cls
@set mesainstalled=1
@IF NOT EXIST "%windir%\System32\mesadrv.dll" IF NOT EXIST "%windir%\System32\graw.dll" IF NOT EXIST "%windir%\System32\osmesa.dll" set mesainstalled=0

@echo Mesa3D system-wide deployment utility
@echo -------------------------------------
@echo Please make a deployment choice:
@echo 1. Desktop OpenGL drivers (softpipe and llvmpipe only);
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x64\swr*.dll" echo 2. Desktop OpenGL drivers (softpipe, llvmpipe and swr drivers);
@echo 3. Mesa3D off-screen render driver gallium version (osmesa gallium);
@IF NOT EXIST "%mesaloc%\x86\osmesa.dll" IF NOT EXIST "%mesaloc%\x64\osmesa.dll" echo 4. Mesa3D off-screen render driver classic version (osmesa swrast);
@echo 5. Mesa3D graw test framework;
@IF %mesainstalled%==1 echo 6. Update system-wide deployment
@IF %mesainstalled%==1 echo 7. Remove system-wide deployments (uninstall);
@IF %mesainstalled%==1 echo 8. Exit
@IF %mesainstalled%==0 echo 6. Exit
@set deploychoice=1
@if "%deploychoice%"=="1" GOTO desktopgl
@if "%deploychoice%"=="2" GOTO desktopgl
@if "%deploychoice%"=="3" GOTO osmesa
@if "%deploychoice%"=="4" GOTO osmesa
@if "%deploychoice%"=="5" GOTO graw
@if "%deploychoice%"=="6" IF %mesainstalled%==1 GOTO update
@if "%deploychoice%"=="7" IF %mesainstalled%==1 GOTO uninstall
@if "%deploychoice%"=="8" IF %mesainstalled%==1 GOTO exit
@if "%deploychoice%"=="6" IF %mesainstalled%==0 GOTO exit
@echo Invaild entry
@GOTO deploy

:desktopgl
@if "%deploychoice%"=="2" if /I NOT %PROCESSOR_ARCHITECTURE%==AMD64 echo Invalid choice. swr driver is only supported on X64/AMD64 systems.
@if "%deploychoice%"=="2" if /I NOT %PROCESSOR_ARCHITECTURE%==AMD64 pause
@if "%deploychoice%"=="2" if /I NOT %PROCESSOR_ARCHITECTURE%==AMD64 GOTO deploy
@if "%deploychoice%"=="2" if /I %PROCESSOR_ARCHITECTURE%==AMD64 IF NOT EXIST "%mesaloc%\x64\swr*.dll" echo Invalid choice. swr driver is not included in MSYS2 Mingw-w64 build of Mesa3D.
@if "%deploychoice%"=="2" if /I %PROCESSOR_ARCHITECTURE%==AMD64 IF NOT EXIST "%mesaloc%\x64\swr*.dll" pause
@if "%deploychoice%"=="2" if /I %PROCESSOR_ARCHITECTURE%==AMD64 IF NOT EXIST "%mesaloc%\x64\swr*.dll" GOTO deploy
@IF /I %PROCESSOR_ARCHITECTURE%==X86 copy "%mesaloc%\x86\opengl32.dll" "%windir%\System32\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x86\opengl32.dll" "%windir%\SysWOW64\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x64\opengl32.dll" "%windir%\System32\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x64\libglapi.dll" copy "%mesaloc%\x64\libglapi.dll" "%windir%\System32"
@if "%deploychoice%"=="2" IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x64\swr*.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "DLL" /t REG_SZ /d "mesadrv.dll" /f
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "DriverVersion" /t REG_DWORD /d "1" /f
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "Flags" /t REG_DWORD /d "1" /f
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "Version" /t REG_DWORD /d "2" /f
@REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "DLL" /t REG_SZ /d "mesadrv.dll" /f
@REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "DriverVersion" /t REG_DWORD /d "1" /f
@REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "Flags" /t REG_DWORD /d "1" /f
@REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /v "Version" /t REG_DWORD /d "2" /f
@echo.
@echo Desktop OpenGL drivers deploy complete.
@GOTO exit

:osmesa
@if "%deploychoice%"=="3" IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%mesaloc%\x86\osmesa.dll" copy "%mesaloc%\x86\osmesa.dll" "%windir%\System32"
@if "%deploychoice%"=="3" IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x86\osmesa.dll" copy "%mesaloc%\x86\osmesa.dll" "%windir%\SysWOW64"
@if "%deploychoice%"=="3" IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x64\osmesa.dll" copy "%mesaloc%\x64\osmesa.dll" "%windir%\System32"
@if "%deploychoice%"=="4" IF EXIST %mesaloc%\x86\osmesa.dll IF EXIST %mesaloc%\x64\osmesa.dll echo Mesa3D was built with Meson so osmesa swrast is not available.
@if "%deploychoice%"=="4" IF EXIST %mesaloc%\x86\osmesa.dll IF EXIST %mesaloc%\x64\osmesa.dll pause
@if "%deploychoice%"=="4" IF EXIST %mesaloc%\x86\osmesa.dll IF EXIST %mesaloc%\x64\osmesa.dll GOTO deploy
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x64\libglapi.dll" copy "%mesaloc%\x64\libglapi.dll" "%windir%\System32"
@if "%deploychoice%"=="3" set osmesatype=gallium
@if "%deploychoice%"=="4" set osmesatype=swrast
@IF /I %PROCESSOR_ARCHITECTURE%==X86 copy "%mesaloc%\x86\osmesa-%osmesatype%\osmesa.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x86\osmesa-%osmesatype%\osmesa.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x64\osmesa-%osmesatype%\osmesa.dll" "%windir%\System32"
@echo.
@echo Off-screen render driver deploy complete.
@GOTO deploy

:graw
@IF /I %PROCESSOR_ARCHITECTURE%==X86 copy "%mesaloc%\x86\graw.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x86\graw.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 copy "%mesaloc%\x64\graw.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%mesaloc%\x86\graw_null.dll" copy "%mesaloc%\x86\graw_null.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x86\graw_null.dll" copy "%mesaloc%\x86\graw_null.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x64\graw_null.dll" copy "%mesaloc%\x64\graw_null.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%mesaloc%\x64\libglapi.dll" copy "%mesaloc%\x64\libglapi.dll" "%windir%\System32"
@echo.
@echo graw framework deploy complete.
@GOTO deploy

:update
@IF %mesainstalled%==0 echo.
@IF %mesainstalled%==0 echo Error: No Mesa3D drivers installed.
@IF %mesainstalled%==0 pause
@IF %mesainstalled%==0 GOTO deploy

@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\mesadrv.dll" copy "%mesaloc%\x86\opengl32.dll" "%windir%\System32\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\mesadrv.dll" copy "%mesaloc%\x86\opengl32.dll" "%windir%\SysWOW64\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\mesadrv.dll" copy "%mesaloc%\x64\opengl32.dll" "%windir%\System32\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\libglapi.dll" IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\libglapi.dll" IF EXIST "%mesaloc%\x86\libglapi.dll" copy "%mesaloc%\x86\libglapi.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\libglapi.dll" IF EXIST "%mesaloc%\x64\libglapi.dll" copy "%mesaloc%\x64\libglapi.dll" "%windir%\System32"
@IF EXIST "%windir%\System32\swrAVX.dll" copy "%mesaloc%\x64\swrAVX.dll" "%windir%\System32"
@IF EXIST "%windir%\System32\swrAVX2.dll" copy "%mesaloc%\x64\swrAVX2.dll" "%windir%\System32"
@IF EXIST "%windir%\System32\swrSKX.dll" copy "%mesaloc%\x64\swrSKX.dll" "%windir%\System32"
@IF EXIST "%windir%\System32\swrKNL.dll" copy "%mesaloc%\x64\swrKNL.dll" "%windir%\System32"

@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\graw.dll" copy "%mesaloc%\x86\graw.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\graw.dll" copy "%mesaloc%\x86\graw.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\graw.dll" copy "%mesaloc%\x64\graw.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\graw.dll" IF EXIST "%mesaloc%\x86\graw_null.dll" copy "%mesaloc%\x86\graw_null.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\graw.dll" IF EXIST "%mesaloc%\x86\graw_null.dll" copy "%mesaloc%\x86\graw_null.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\graw.dll" IF EXIST "%mesaloc%\x64\graw_null.dll" copy "%mesaloc%\x64\graw_null.dll" "%windir%\System32"

@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\osmesa.dll" IF EXIST "%mesaloc%\x86\osmesa.dll" copy "%mesaloc%\x86\osmesa.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\osmesa.dll" IF EXIST "%mesaloc%\x86\osmesa.dll" copy "%mesaloc%\x86\osmesa.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\osmesa.dll" IF EXIST "%mesaloc%\x64\osmesa.dll" copy "%mesaloc%\x64\osmesa.dll" "%windir%\System32"
@IF EXIST "%windir%\System32\osmesa.dll" IF EXIST "%mesaloc%\x86\osmesa.dll" IF EXIST "%mesaloc%\x64\osmesa.dll" GOTO doneupdate
@set BYTES=10000000
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\osmesa.dll" for %%f in ("%windir%\System32\osmesa.dll") do @set BYTES=%%~zf
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\osmesa.dll" IF %BYTES% GTR 10000000 copy "%mesaloc%\x86\osmesa-gallium\osmesa.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==X86 IF EXIST "%windir%\System32\osmesa.dll" IF %BYTES% LSS 10000000 copy "%mesaloc%\x86\osmesa-swrast\osmesa.dll" "%windir%\System32"
@set BYTES=10000000
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\osmesa.dll" for %%f in ("%windir%\SysWOW64\osmesa.dll") do @set BYTES=%%~zf
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\osmesa.dll" IF %BYTES% GTR 10000000 copy "%mesaloc%\x86\osmesa-gallium\osmesa.dll" "%windir%\SysWOW64"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\osmesa.dll" IF %BYTES% LSS 10000000 copy "%mesaloc%\x86\osmesa-swrast\osmesa.dll" "%windir%\SysWOW64"
@set BYTES=10000000
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\osmesa.dll" for %%f in ("%windir%\System32\osmesa.dll") do @set BYTES=%%~zf
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\osmesa.dll" IF %BYTES% GTR 10000000 copy "%mesaloc%\x64\osmesa-gallium\osmesa.dll" "%windir%\System32"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\System32\osmesa.dll" IF %BYTES% LSS 10000000 copy "%mesaloc%\x64\osmesa-swrast\osmesa.dll" "%windir%\System32"

:doneupdate
@echo.
@echo Update complete.
@GOTO deploy

:uninstall
@REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /f
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 REG DELETE "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\OpenGLDrivers\MSOGL" /f
@IF EXIST "%windir%\System32\mesadrv.dll" del "%windir%\System32\mesadrv.dll"
@IF EXIST "%windir%\System32\libglapi.dll" del "%windir%\System32\libglapi.dll"
@IF EXIST "%windir%\System32\graw.dll" del "%windir%\System32\graw.dll"
@IF EXIST "%windir%\System32\graw_null.dll" del "%windir%\System32\graw_null.dll"
@IF EXIST "%windir%\System32\osmesa.dll" del "%windir%\System32\osmesa.dll"
@IF EXIST "%windir%\System32\swrAVX.dll" del "%windir%\System32\swrAVX.dll"
@IF EXIST "%windir%\System32\swrAVX2.dll" del "%windir%\System32\swrAVX2.dll"
@IF EXIST "%windir%\System32\swrSKX.dll" del "%windir%\System32\swrSKX.dll"
@IF EXIST "%windir%\System32\swrKNL.dll" del "%windir%\System32\swrKNL.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\mesadrv.dll" del "%windir%\SysWOW64\mesadrv.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\libglapi.dll" del "%windir%\SysWOW64\libglapi.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\osmesa.dll" del "%windir%\SysWOW64\osmesa.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\graw.dll" del "%windir%\SysWOW64\graw.dll"
@IF /I %PROCESSOR_ARCHITECTURE%==AMD64 IF EXIST "%windir%\SysWOW64\graw_null.dll" del "%windir%\SysWOW64\graw_null.dll"
@echo.
@echo Uninstall complete.
@GOTO deploy

:exit
@echo Good Bye!
@exit