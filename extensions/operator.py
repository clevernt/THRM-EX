import lightbulb
import hikari
import requests
import re

from utils.operator import create_embed, fetch_operator_data
from typing import Sequence, Union

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("operator")

operators = requests.get("https://awedtan.ca/api/operator?include=keys").json()


@plugin.command
@lightbulb.option("operator", "Operator", required=True, autocomplete=True)
@lightbulb.command("operator", "operator info", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def operator(ctx: lightbulb.SlashContext):
    api_resp = fetch_operator_data(ctx.options.operator)
    embeds = create_embed(api_resp)
    await ctx.respond(embeds=embeds)


@operator.autocomplete("operator")
async def operator_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_operators = [
        operator for operator in operators if user_input in operator["keys"][1]
    ]
    matching_operators = matching_operators[:25]
    return [
        hikari.CommandChoice(name=operator["keys"][1], value=operator["keys"][1])
        for operator in matching_operators
    ]


def load(bot):
    bot.add_plugin(plugin)
