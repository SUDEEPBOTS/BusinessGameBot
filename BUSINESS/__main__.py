import asyncio
from BUSINESS.core.bot import app

async def main():
    await app.start()
    print(f"Business Bot is now running!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
