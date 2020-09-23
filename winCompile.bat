IF EXIST "Logician.exe" (
    DEL "Logician.exe"
)
pyinstaller main.spec -w -F
MOVE /y .\dist\Logician.exe .\Logician.exe
RMDIR .\dist /s /q
RMDIR .\build /s /q