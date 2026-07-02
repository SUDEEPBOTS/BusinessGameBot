import logging
from pyrogram import Client, __version__
import config
from BUSINESS.core import monkeypatch

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("business.log"), logging.StreamHandler()],
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

class BusinessBot(Client):
    def __init__(self):
        logger.info("Initializing Business Bot...")
        super().__init__(
            name="BusinessBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="BUSINESS.plugins"),
        )

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        logger.info(f"Bot Started as {self.me.first_name} (@{self.me.username})")

    async def stop(self):
        await super().stop()
        logger.info("Bot Stopped.")

app = BusinessBot()