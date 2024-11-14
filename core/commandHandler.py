from .commands.command import Command

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self,command: Command):
        self.commands[command.name] = command
    
    async def execute_command(self,command_name: str, args, ctx):
        command = self.commands.get(command_name) #get Command object from list of commands
        command_require_args = hasattr(command,'syntax')

        if not command: 
            await ctx.reply(f'Command: {command_name} not found. For list of avaliable commands type $cmds')
            return

        if command_require_args and not args:
            #TODO: improve it to check for number of args command requires
            await ctx.reply(f'Please use correct syntax. {command.syntax}')
            return
        
        await command.execute(ctx, *args)
        
            