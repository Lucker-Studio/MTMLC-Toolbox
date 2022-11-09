@echo off
pyinstaller Omegar-Toolbox.spec --distpath build --workpath build\temp
cd build
rd /s /q temp
ren Omegar-Toolbox.exe Omegar-Toolbox-Windows.exe
