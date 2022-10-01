import lightbulb
from dotenv import load_dotenv
import os
import miru
load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv('token')
)
miru.load(bot)

bot.load_extensions_from('./extensions')

bot.run()