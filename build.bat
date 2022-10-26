@echo off
pipenv run pyinstaller Omegar-Toolbox.spec --distpath building\windows --workpath building\windows\temp
wsl python -m pipenv run pyinstaller Omegar-Toolbox.spec --distpath building/linux --workpath building/linux/temp