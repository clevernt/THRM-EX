import lightbulb

plugin = lightbulb.Plugin('ping')

@plugin.command
@lightbulb.command('ping', "Gives you the bot's ping")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f"Pong! **{plugin.bot.heartbeat_latency * 1_000:.0f}ms**")
    
def load(bot):
    bot.add_plugin(plugin)