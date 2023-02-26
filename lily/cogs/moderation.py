import asyncio
import discord
from discord import app_commands, Interaction, User, Member, Color, Embed
from discord.ext import commands
from rojitzu.utils.extentsions import PrismaExt
from rojitzu.utils.utilities import UtilMethods
from rojitzu.models.infractions import InfractionManager, InfractionType
from typing import Union


class Moderation(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.client = bot
        self.prisma = PrismaExt()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect_client())
        self.infraction_manager = InfractionManager(self.client, self.prisma)

    @app_commands.command(name="warn", description="Warns a member")
    async def warn(self, interaction: Interaction, target: Union[User, Member], reason: str) -> None:
        await self.infraction_manager.create_infraction(InfractionType.WARN, interaction.user, target, reason)
        await interaction.response.send_message(f"{target.name} has been warned", ephemeral=True)

    @app_commands.command(name="warnings", description="Lists user warnings")
    async def warnings(self, interaction: Interaction, user: Union[User, Member]) -> None:
        warns = await self.infraction_manager.list_infractions(InfractionType.WARN, user)
        if not warns:
            embed = await UtilMethods.embedify("Warnings", f"{user.name} has no warnings", Color.blurple())
        else:
            embed = Embed(title="Warnings", color=Color.blue())
            for i, warn in enumerate(warns):
                embed.add_field(name=f"Warning {i + 1}", value=f"Moderator: ``{warn.target.name}``\nWarned: "
                                                               f"``{warn.infractor.name}``\nReason: **{warn.reason}**")
        await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(Moderation(bot))
