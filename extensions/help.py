import lightbulb
import hikari

plugin = lightbulb.Plugin('help')

@plugin.command
@lightbulb.command('help', 'commands list', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    embed = hikari.Embed(title='Commands List')
    embed.add_field('Arknights', "`arkrec`, `module`")
    embed.add_field('Misc', "`ping`")
    await ctx.respond(embed)

def load(bot):
    bot.add_plugin(plugin)