import lightbulb
from dotenv import load_dotenv
import os
load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv('TEST_TOKEN'),
    help_slash_command=True
)

bot.load_extensions_from('./extensions')

bot.run()
