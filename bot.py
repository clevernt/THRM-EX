import lightbulb

bot = lightbulb.BotApp(
    token=TOKEN
)

bot.load_extensions_from('./extensions')

bot.run()