import lightbulb
import os

from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    help_slash_command=True
)

bot.load_extensions_from("extensions")

bot.run()
