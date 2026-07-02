import yaml
import os

STRINGS = {}

def load_strings():
    strings_dir = os.path.join(os.path.dirname(__file__), "strings")
    for file in os.listdir(strings_dir):
        if file.endswith(".yml"):
            lang = file.split(".")[0]
            with open(os.path.join(strings_dir, file), "r", encoding="utf-8") as f:
                STRINGS[lang] = yaml.safe_load(f)

load_strings()

def get_string(lang: str, key: str) -> str:
    # Fallback to english if language or key not found
    if lang not in STRINGS:
        lang = "en"
    
    return STRINGS[lang].get(key, STRINGS["en"].get(key, f"Missing string: {key}"))
