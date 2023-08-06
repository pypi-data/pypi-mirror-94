import os
import logging

import discord

dbb_logger = logging.getLogger("discord-base-bots")
logging.getLogger("discord-base-bots").addHandler(logging.NullHandler())
# To turn off logging: logging.getLogger("discord-base_bots").propagate = False


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
        dbb_logger.debug(f'{self.bot_name} online')

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
                try:
                    await command(command_content, message)
                except Exception as e:
                    dbb_logger.exception("Failed executing command")


def run_bot(bot_class, dotenv_path=None):
    if dotenv_path:
        if os.path.exists(dotenv_path):
            import dotenv
            dotenv.load_dotenv(dotenv_path=dotenv_path)
        else:
            raise ValueError(f"{dotenv_path} file not found")

    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("DISCORD_TOKEN not found in environment variables")

    intents = discord.Intents.default()
    intents.members = True

    client = bot_class(intents=intents)
    client.run(token)


if __name__ == "__main__":
    from pathlib import Path

    class SimpleBot(BaseBot):
        bot_name = "SimpleBot"
        hot_word = "simplebot"

    run_bot(SimpleBot, Path(".env").resolve())
