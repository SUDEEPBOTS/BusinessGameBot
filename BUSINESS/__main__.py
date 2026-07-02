import asyncio
from BUSINESS.core.bot import app
from BUSINESS import config

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