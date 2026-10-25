@echo off
cd /d "%~dp0"
echo ========================================================
echo Compilando Comprension_Contexto_Audiencia_Tecnica_Proyecto2.tex...
echo ========================================================

set COMPILER="%USERPROFILE%\bin\tectonic.exe"
if not exist %COMPILER% set COMPILER="%~dp0..\..\bin\tectonic.exe"
if not exist %COMPILER% set COMPILER=tectonic

%COMPILER% Comprension_Contexto_Audiencia_Tecnica_Proyecto2.tex
if %errorlevel% equ 0 (
    echo.
    echo [EXITO] PDF generado exitosamente: Comprension_Contexto_Audiencia_Tecnica_Proyecto2.pdf
) else (
    echo.
    echo [ERROR] Hubo un problema durante la compilacion.
)
pause
