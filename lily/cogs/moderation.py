from __future__ import annotations
import asyncio
import discord
from discord import app_commands, Interaction, User, Member, Color, Embed, SelectOption, HTTPException
from discord.ext import commands
from lily.utils.extentsions import PrismaExt
from lily.utils.utilities import UtilMethods
from lily.models.infractions import InfractionManager, InfractionType
from lily.models.views import InfractionRemove
from typing import Union, List, Optional


class Moderation(commands.Cog):
    group = app_commands.Group(name="infraction", description="Infraction commands")

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())
        self.infraction_manager = InfractionManager(self.client, self.prisma)

    async def type_autocomplete(self, interaction: Interaction, current: str) -> List[app_commands.Choice]:
        return [app_commands.Choice(name=infraction_type.value.capitalize(), value=infraction_type.value)
                for infraction_type in InfractionType if current.lower() in infraction_type.value.lower()]

    @app_commands.command(name="warn", description="Warns a member")
    async def warn(self, interaction: Interaction, target: Union[User, Member], reason: str) -> None:
        await self.infraction_manager.create_infraction(InfractionType.WARN, interaction.user, target, reason)
        await interaction.response.send_message(f"{target.name} has been warned", ephemeral=True)

    @group.command(name="list", description="Lists user infractions")
    @app_commands.autocomplete(infraction=type_autocomplete)
    async def infractions(self, interaction: Interaction, user: Union[User, Member], infraction: Optional[str]) -> None:
        args = [user]
        if infraction:
            args.append(InfractionType(infraction))
        infractions = await self.infraction_manager.list_infractions(*args)
        embed = await self.infraction_manager.infractions_embed(user, infractions, infraction)
        await interaction.response.send_message(embed=embed)

    @group.command(name="remove", description="Remove user infraction")
    @app_commands.autocomplete(infraction=type_autocomplete)
    async def remove(self, interaction: Interaction, user: Union[User, Member], infraction: str) -> None:
        infractions = await self.infraction_manager.list_infractions(user, InfractionType(infraction))
        view = InfractionRemove(self.infraction_manager,
                                [SelectOption(label=inf.id, value=inf.id, emoji='???') for inf in infractions])
        try:
            embed = await self.infraction_manager.infractions_embed(user, infractions, infraction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except HTTPException as e:
            embed = Embed(title="Important", description=f"{user.name} does not have any {infraction}s",
                          color=Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
