import lightbulb
from dotenv import load_dotenv
import os
load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv('token'),
)

bot.load_extensions_from('./extensions')

bot.run()