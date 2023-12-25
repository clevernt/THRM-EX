import lightbulb
import hikari

plugin = lightbulb.Plugin("ping")


@plugin.command
@lightbulb.command("ping", "Check bot's ping")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    embed = hikari.Embed(
        title="Pong!", description=f"**{plugin.bot.heartbeat_latency * 1_000:.0f}ms**"
    )
    embed.add_field("Currently in", f"{plugin.bot.cache.get_guilds_view()} guilds!")
    await ctx.respond(embed)


def load(bot):
    bot.add_plugin(plugin)
