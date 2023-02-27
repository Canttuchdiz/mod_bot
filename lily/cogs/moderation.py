from __future__ import annotations
import asyncio
import discord
from discord import app_commands, Interaction, User, Member, Color, Embed
from discord.ext import commands
from lily.utils.extentsions import PrismaExt
from lily.utils.utilities import UtilMethods
from lily.models.infractions import InfractionManager, InfractionType
from typing import Union, List, Optional


class Moderation(commands.Cog):
    group = app_commands.Group(name="infraction", description="Infraction commands")

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())
        self.infraction_manager = InfractionManager(self.client, self.prisma)

    async def infraction_autocomplete(self, interaction: Interaction, current: str) -> List[app_commands.Choice]:
        return [app_commands.Choice(name=infraction_type.value.capitalize(), value=infraction_type.value) for infraction_type in InfractionType if current.lower() in infraction_type.value.lower()]

    @app_commands.command(name="warn", description="Warns a member")
    async def warn(self, interaction: Interaction, target: Union[User, Member], reason: str) -> None:
        await self.infraction_manager.create_infraction(InfractionType.WARN, interaction.user, target, reason)
        await interaction.response.send_message(f"{target.name} has been warned", ephemeral=True)

    @group.command(name="list", description="Lists user infractions")
    @app_commands.autocomplete(infraction=infraction_autocomplete)
    async def infractions(self, interaction: Interaction, user: Union[User, Member], infraction: Optional[str]) -> None:
        args = [user]
        if infraction:
            args.append(InfractionType(infraction))
        infractions = await self.infraction_manager.list_infractions(*args)
        if not infractions:
            embed = await UtilMethods.embedify("Infractions", f"{user.name} has no {infraction}s", Color.blurple())
        else:
            embed = Embed(title="Infractions", color=Color.blue())
            for i, inf in enumerate(infractions):
                embed.add_field(name=f"{inf.type.value.capitalize()} {i + 1}",
                                value=f"Moderator: ``{inf.target.name}``\nTarget: "
                                      f"``{inf.infractor.name}``\nReason: **{inf.reason}**\nID: *{inf.id}*")
            embed.set_footer(text=f"ID · {infractions[0].target.id}")
        await interaction.response.send_message(embed=embed)

    # @group.command(name="remove", description="Remove user infraction")
    # @app_commands.autocomplete(infraction=infraction_autocomplete)
    # async def remove(self, interaction: Interaction, user: Union[User, Member], infraction: str) -> None:
    #     pass


async def setup(bot):
    await bot.add_cog(Moderation(bot))
