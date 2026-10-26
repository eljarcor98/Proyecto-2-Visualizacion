@echo off
cd /d "%~dp0"
echo ========================================================
echo Compilando EquipoX_Proyecto2_Resumen.tex con Tectonic...
echo ========================================================

set COMPILER="%~dp0..\..\bin\tectonic.exe"
if not exist %COMPILER% set COMPILER="%USERPROFILE%\bin\tectonic.exe"
if not exist %COMPILER% set COMPILER=tectonic

%COMPILER% EquipoX_Proyecto2_Resumen.tex
if %errorlevel% equ 0 (
    echo.
    echo [EXITO] PDF generado exitosamente: EquipoX_Proyecto2_Resumen.pdf
) else (
    echo.
    echo [ERROR] Hubo un problema durante la compilacion.
)
pause
