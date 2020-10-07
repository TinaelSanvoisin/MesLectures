import os
from pathlib import Path
import json

MESLECTURES_DIR = os.path.join(Path.home(), ".mesLectures")
MESLECTURES_FILE = os.path.join(MESLECTURES_DIR,"books.json")