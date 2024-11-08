from .commands import Command

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self,command: Command):
        self.commands[command.name] = command
    
    async def execute_command(self,command_name: str, args, ctx):
        command = self.commands.get(command_name)
        if command:
            await command.execute(ctx, *args)
        else:
            await ctx.send(f'Command: {command_name} not found. For list of avaliable commands type $cmds')
