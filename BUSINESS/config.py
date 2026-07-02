import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "25547055"))
API_HASH = os.environ.get("API_HASH", "f75d5ba7348bf1297eefd0a7a3b342fb")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://sudeep:sudeep@cluster0.p1bns.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(os.environ.get("OWNER_ID", "8742583469"))

# Web Server / Keep-Alive Configuration
RENDER_DEPLOY = os.environ.get("RENDER_DEPLOY", "True").lower() == "true"
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:8080")

# Logging
LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1001234567890"))

# Styling options
START_IMG_URL = "https://m.media-amazon.com/images/I/61Z-o453tsL._AC_UF1000,1000_QL80_.jpg"
