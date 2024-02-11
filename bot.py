import lightbulb
import hikari
import os

from dotenv import load_dotenv

load_dotenv()

bot = lightbulb.BotApp(token=os.getenv("TEST_TOKEN"), help_slash_command=True)

bot.load_extensions_from("extensions")

bot.run()
print(bot.cache.get_guilds_view())
