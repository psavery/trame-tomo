pyinstaller ^
  --hidden-import vtkmodules.all ^
  --collect-data pywebvue ^
  --onefile ^
  --windowed ^
  --icon trame-tomo.ico ^
  .\run.py
