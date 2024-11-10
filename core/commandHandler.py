from .commands.command import Command

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self,command: Command):
        self.commands[command.name] = command
    
    async def execute_command(self,command_name: str, args, ctx):
        command = self.commands.get(command_name) #get Command object from list of commands
        if not command: 
            #if command doesn't exist, notify user
            await ctx.reply(f'Command: {command_name} not found. For list of avaliable commands type $cmds')
            return

        if hasattr(command,'syntax') and not args:
            #if command requires args but none provided notify user
            #TODO: improve it to check for number of args command requires
            await ctx.reply(f'Please use correct syntax. {command.syntax}')
            return
        
        await command.execute(ctx, *args)
        
            