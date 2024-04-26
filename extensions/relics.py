import lightbulb
import hikari

from typing import Sequence, Union
from lightbulb.utils import pag, nav

from utils.relics import get_relic_details, get_relic_icon, relics_data, rogue_mapping
from utils.data import EMBED_COLOR

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("relic")


@plugin.command
@lightbulb.option("relic", "Relic, foldartal, etc", required=True, autocomplete=True)
@lightbulb.command("relic", "Get details about a relic or a foldartal", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def relic(ctx):
    paginator = pag.EmbedPaginator()
    relics_list = get_relic_details(ctx.options.relic)
    embeds = []
    for relic in relics_list:
        relic_icon = get_relic_icon(relic["iconId"])

        embed = hikari.Embed(
            title=relic["name"],
            color=EMBED_COLOR,
        )

        embed.set_author(name=relic["rogue"])
        embed.set_thumbnail(relic_icon)
        embed.set_footer(relic["description"])
        embed.add_field("Usage", relic["usage"])
        embed.add_field("Unlock Condition", relic["unlockCond"])

        embeds.append(embed)

        paginator.add_line(embed)
    navigator = nav.ButtonNavigator(embeds)
    await navigator.run(ctx)


@relic.autocomplete("relic")
async def enemy_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower().strip()

    matching_relics = []
    for rogue_key, _ in rogue_mapping.items():
        items = relics_data.get("details", {}).get(rogue_key, {}).get("items", {})
        for _, relic_details in items.items():
            if relic_details.get("name", "").strip("'").lower().startswith(user_input):
                matching_relics.append(relic_details.get("name"))

    matching_relics = matching_relics[:25]

    return [hikari.CommandChoice(name=relic, value=relic) for relic in matching_relics]


def load(bot):
    bot.add_plugin(plugin)
