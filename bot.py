import lightbulb
import os

from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    help_slash_command=True,
    default_enabled_guilds=753858152486797352,
)

bot.load_extensions_from("extensions")

bot.run()
