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

import asyncio
import BUSINESS.core.monkeypatch # Essential for Kurigram button colors & emojis
from BUSINESS.core.bot import app
import config

async def main():
    if config.RENDER_DEPLOY:
        try:
            from server import keep_alive
            await keep_alive()
        except Exception as e:
            print(f"Failed to start web server: {e}")

    await app.start()
    print(f"Business Bot is now running!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())