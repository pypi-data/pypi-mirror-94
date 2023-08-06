import os
from dotenv import load_dotenv
from pathlib import Path


def get_env(env_name: str) -> str:
    load_dotenv(verbose=True)
    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    except:
        dotenv_path = os.path.join(Path().resolve(), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(env_name)
