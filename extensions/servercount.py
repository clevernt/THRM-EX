import lightbulb
import hikari

plugin = lightbulb.Plugin("servercount")


@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("servercount", "Check Servers Count")
@lightbulb.implements(lightbulb.SlashCommand)
async def servercount(ctx):
    await ctx.respond(list(ctx.bot.cache.get_guilds_view().items()))


def load(bot):
    bot.add_plugin(plugin)
