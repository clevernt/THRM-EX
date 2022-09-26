import lightbulb

bot = lightbulb.BotApp(
    token='NTI2Njk3MjQyOTgwMjUzNjk2.GGYpSZ.eHGhSnQUKlUjAHy2kvfnmH7NnT6bI2JIh4wmw4',
)

bot.load_extensions_from('./extensions')

bot.run()