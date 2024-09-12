import lightbulb
import hikari
import miru

from typing import Sequence, Union
from lightbulb.utils import pag, nav

from utils.relics import get_relic_details, get_relic_icon, relics_data, rogue_mapping
from utils.data import EMBED_COLOR

plugin = lightbulb.Plugin("relic")


class SelectMenu(miru.TextSelect):
    def __init__(self, relics, options) -> None:
        self.relics = relics
        super().__init__(options=options, placeholder="Choose IS Season")

    async def callback(self, ctx: miru.ViewContext) -> None:
        selected_index = int(self.values[0])
        selected_relic = self.relics[selected_index]

        await ctx.edit_response(selected_relic)


class ISSelector(miru.View):
    def __init__(self, relics: list, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.relics = relics

        options = [
            miru.SelectOption(
                label=relic.author.name,
                value=str(i),
                description=None,
                emoji=None,
                is_default=False,
            )
            for i, relic in enumerate(relics)
        ]
        selector = SelectMenu(relics=self.relics, options=options)
        self.add_item(selector)


@plugin.command
@lightbulb.option("relic", "Relic, foldartal, etc", required=True, autocomplete=True)
@lightbulb.command("relic", "Get details about a relic or a foldartal", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def relic(ctx):
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

        if relic["unlockCond"]:
            embed.add_field("Unlock Condition", relic["unlockCond"])

        embeds.append(embed)

    view = ISSelector(embeds)
    await ctx.respond(embeds[0], components=view)
    plugin.app.d.miru.start_view(view)


@relic.autocomplete("relic")
async def enemy_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower().strip()

    matching_relics = []
    for rogue_key, _ in rogue_mapping.items():
        items = relics_data.get("details", {}).get(rogue_key, {}).get("items", {})
        for _, relic_details in items.items():
            if user_input in relic_details.get("name", "").strip("'").lower():
                matching_relics.append(relic_details.get("name"))

    matching_relics = matching_relics[:25]

    return [hikari.CommandChoice(name=relic, value=relic) for relic in matching_relics]


def load(bot):
    bot.add_plugin(plugin)
