from ..command import Command
import discord

class CmdsCommand(Command):

    def __init__(self, commands):
        self.commands = commands
        super().__init__(name="cmds",description="Displays all valid commands for NaviBot.")

    async def execute(self, ctx, *args):
        await ctx.reply(embed=self.build_embed())

    def build_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"Commands",
            colour=0x00b0f4
        )
        embed.set_author(name="NaviBot")
        
        for command in self.commands.values():
            embed.add_field(name=f"{command.syntax if hasattr(command,'syntax') else '$' + command.name}", value=f"``{command.description}``" or "``N/A``", inline=False)
        

        return embed

   
            