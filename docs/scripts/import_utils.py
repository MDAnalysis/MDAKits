import sys
import pathlib

UTILS_DIR = pathlib.Path(__file__).parent.parent.parent.resolve() / "utils"
sys.path.insert(0, str(UTILS_DIR))

from mdakit import MDAKit

