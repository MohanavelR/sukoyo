from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class Settings:
    X=50
    Y=50
    WIDTH=1300
    HEIGHT=700
    TITLE="Sukoyo"
    ROOT_PATH=Path(__file__).parent.parent.parent.resolve()
    