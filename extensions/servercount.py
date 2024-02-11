import lightbulb
import hikari

plugin = lightbulb.Plugin("servercount")


@plugin.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.command("servercount", "Check Servers Count")
@lightbulb.implements(lightbulb.SlashCommand)
async def servercount(ctx):
    embed = hikari.Embed(
        description=f"Currently in {ctx.bot.cache.get_guilds_view().values()}"
    )
    await ctx.respond(embed)


def load(bot):
    bot.add_plugin(plugin)
