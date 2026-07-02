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

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "25547055"))
API_HASH = os.environ.get("API_HASH", "f75d5ba7348bf1297eefd0a7a3b342fb")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://sudeep:sudeep@cluster0.p1bns.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(os.environ.get("OWNER_ID", "8742583469"))


RENDER_DEPLOY = os.environ.get("RENDER_DEPLOY", "True").lower() == "true"
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:8080")


LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1001234567890"))


SUDOERS = [OWNER_ID]
BANNED_USERS = []


START_IMG_URL = "https://m.media-amazon.com/images/I/61Z-o453tsL._AC_UF1000,1000_QL80_.jpg"