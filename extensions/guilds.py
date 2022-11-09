import lightbulb
from lightbulb.utils.pag import StringPaginator

plugin = lightbulb.Plugin('guilds')

@plugin.command()
@lightbulb.command('guilds', 'List of Guilds the bot is in.', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def guilds(ctx):
    guilds = await plugin.rest.fetch_my_guilds()
    pag = StringPaginator(max_lines=10)
    for n, guild in enumerate(guilds, start=1):
        pag.add_line(f"**{n}.** {guild.name}")
    for page in pag.build_pages():
        await ctx.respond(page)

    
def load(bot):
    bot.add_plugin(plugin)