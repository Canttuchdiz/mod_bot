from __future__ import annotations
import discord
from discord import User, Member
from discord.ext import commands
from dataclasses import dataclass
from rojitzu.utils.extentsions import PrismaExt
from typing import Union, List
from enum import Enum


class InfractionType(Enum):
    WARN = "warn"
    TIMEOUT = "timeout"
    KICK = "kick"
    BAN = "ban"


@dataclass
class Infraction:
    type: InfractionType
    infractor: Union[User, Member]
    target: Union[User, Member]
    reason: str


class InfractionManager:

    def __init__(self, bot: commands.Bot, prisma: PrismaExt) -> None:
        self.client = bot
        self.prisma = prisma

    async def create_infraction(self, infraction_type: InfractionType, infractor: Union[User, Member], target: Union[User, Member], reason: str) -> Infraction:
        await self.prisma.infraction.create(
            data={
                'type': infraction_type.value,
                'infractorid': infractor.id,
                'targetid': target.id,
                'reason': str(reason)
            }
        )
        return Infraction(infraction_type, infractor, target, reason)

    async def list_infractions(self, infraction_type: InfractionType, target: Union[Member, User]) -> List[Infraction]:
        infractions = await self.prisma.infraction.find_many(
            where={
                "type": infraction_type.value,
                "targetid": target.id
            }
        )
        return [Infraction(infraction_type, self.client.get_user(infraction.infractorid),
                           target, infraction.reason) for infraction in infractions]




