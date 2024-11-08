from __future__ import annotations
from discord.ext import commands
from .commands import *
from .CommandHandler import CommandHandler
import discord

__all__ = (
    "Bot",
)

class Bot(commands.AutoShardedBot):

    handler = CommandHandler()
    handler.register_command(MetarCommand())
    handler.register_command(CmdsCommand())

    def __init__(self):
        super().__init__(
            command_prefix = "?",
            intents=discord.Intents.all(),
            chunk_build_at_startup=False
        )

    async def on_ready(self) -> None:
        print(f'logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('$'):
            parts = message.content.split(maxsplit=1)
            command = parts[0][1:].lower()
            args = parts[1].split() if len(parts) > 1 else []
            ctx = await self.get_context(message)
            await self.handler.execute_command(command, args, ctx)


            