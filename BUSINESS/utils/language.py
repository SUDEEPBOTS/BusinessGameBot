# Copyright (c) 2025 @SUDEEPBOTS <HellfireDevs>
# Location: delhi,noida
#
# All rights reserved.
#
# This code is the intellectual property of SUDEEPBOTS.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: sudeepgithub@gmail.com

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
    if lang not in STRINGS:
        lang = "en"
    return STRINGS[lang].get(key, STRINGS["en"].get(key, f"Missing string: {key}"))