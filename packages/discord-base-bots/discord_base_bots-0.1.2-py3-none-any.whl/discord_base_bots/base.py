import os
import discord


class BaseBot(discord.Client):

    bot_name = None
    hot_word = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # command string: function object
        # "roll": self.roll
        self.commands = {
        }

    def update_commands(self, commands):
        self.commands.update(commands)

    async def on_ready(self):
        print(f'{self.bot_name} online')

    async def on_message(self, message):
        if message.content.lower().startswith(self.hot_word):
            void, command_and_data = message.content.split(sep=None, maxsplit=1)
            command = None
            command_content = None
            for command_name, command_func in self.commands.items():
                if command_and_data.lower().startswith(command_name):
                    command = command_func
                    command_content = command_and_data.split(command_name, maxsplit=1)[-1].strip()
                    break
            if command is not None:
                await command(command_content, message)


def run_bot(bot_class, dot_env_path):
    if os.path.exists(dot_env_path):
        import dotenv
        dotenv.load_dotenv()

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.members = True

    client = bot_class(intents=intents)
    client.run(TOKEN)


if __name__ == "__main__":
    from pathlib import Path

    class SimpleBot(BaseBot):
        bot_name = "SimpleBot"
        hot_word = "simplebot"

    run_bot(SimpleBot, Path(".env").resolve())
