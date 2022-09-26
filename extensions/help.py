import lightbulb
import hikari

plugin = lightbulb.Plugin('help')

@plugin.command
@lightbulb.command('help', 'commands list')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    embed = hikari.Embed(title='Commands List')
    embed.add_field('🎮 Arknights', "`arkrec`, `module`")
    await ctx.respond(embed)

def load(bot):
    bot.add_plugin(plugin)