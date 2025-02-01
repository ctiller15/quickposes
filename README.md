## Quickposes

An application built in tkinter to do quickposes

## Getting started

```
python3 -m venv quick_poses_virtualenv
source quick_poses_virtualenv/bin/activate
```

```
chmod +x ./start.sh
./start.sh
```

## Build
```bash
# macos
pyinstaller -n="QuickPoses" --windowed --icon=icon.ico main.py
```