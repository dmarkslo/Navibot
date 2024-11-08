import discord
from core import Bot
from config import TOKEN
import asyncio

async def main():
    discord.utils.setup_logging()
    async with Bot() as bot:
        await bot.start(TOKEN)


asyncio.run(main())