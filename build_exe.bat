:: build game
@echo Start Virtual Enviroment
cd lc-venv\Scripts
call activate.bat
cd ../..
@echo Build EXE
pyinstaller game.py --onefile --noconsole
@echo Move exe to root
move /Y dist\game.exe game.exe
@echo Exit Virtual Enviroment
deactivate
pause
