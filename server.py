from aiohttp import web
import asyncio
import logging
import aiohttp
import config

logger = logging.getLogger(__name__)

async def handle(request):
    return web.Response(text="Business Game Bot is running 24/7!")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("Web server started on port 8080")

async def ping_server():
    while True:
        await asyncio.sleep(5 * 60) # Ping every 5 minutes
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(config.RENDER_EXTERNAL_URL) as response:
                    if response.status == 200:
                        logger.info("Pinged successfully to keep server alive.")
                    else:
                        logger.warning(f"Ping failed with status: {response.status}")
        except Exception as e:
            logger.error(f"Error pinging server: {e}")

async def keep_alive():
    await web_server()
    asyncio.create_task(ping_server())
