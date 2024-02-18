import pathlib
import sys

for path in pathlib.Path(__file__).parent.parent.iterdir():
    if path.is_dir():
        sys.path.append(str(path.absolute()))
