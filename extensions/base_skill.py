import lightbulb
import hikari
import requests

from typing import Sequence, Union
from utils.data import EMBED_COLOR, operators, GITHUB_REPO
from utils.base_skill import get_operator_data, extract_base_skills, create_embeds

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("base_skill")


@plugin.command
@lightbulb.option("operator", "Operator name", required=True, autocomplete=True)
@lightbulb.command("baseskill", "Get an operator's base skill(s)", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def base_skill(ctx):
    operator = ctx.options.operator
    operator_data = get_operator_data(operator)
    if not operator_data:
        await ctx.respond(hikari.Embed(description=f"Operator `{operator}` not found."))
        return

    base_skills = extract_base_skills(operator_data)
    embeds = create_embeds(base_skills)

    char_id = (
        requests.get(f"https://awedtan.ca/api/operator/{operator.lower()}?include=id")
        .json()
        .get("value")
        .get("id")
    )
    char_av = f"{GITHUB_REPO}/avatar/ASSISTANT/{char_id}_2.png"
    char_embed = hikari.Embed(title=operator.title(), color=EMBED_COLOR).set_thumbnail(
        char_av
    )
    embeds.insert(0, char_embed)
    await ctx.respond(embeds=embeds)


@base_skill.autocomplete("operator")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_operators = [
        operator for operator in operators if user_input in operator.lower()
    ]
    matching_operators = matching_operators[:25]
    return [
        hikari.CommandChoice(name=operator, value=operator)
        for operator in matching_operators
    ]


def load(bot):
    bot.add_plugin(plugin)
