import lightbulb
from dotenv import load_dotenv
import os
load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv('token'),
    default_enabled_guilds=753858152486797352
)

bot.load_extensions_from('./extensions')

bot.run()