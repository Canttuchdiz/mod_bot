from __future__ import annotations
import discord
from discord import User, Member
from discord.ext import commands
from dataclasses import dataclass
from lily.utils.extentsions import PrismaExt
from typing import Union, List, Optional
from enum import Enum


class InfractionType(Enum):
    WARN = "warn"
    TIMEOUT = "timeout"
    KICK = "kick"
    BAN = "ban"


@dataclass
class Infraction:
    id: str
    type: InfractionType
    infractor: Union[User, Member]
    target: Union[User, Member]
    reason: str


class InfractionManager:

    def __init__(self, bot: commands.Bot, prisma: PrismaExt) -> None:
        self.client = bot
        self.prisma = prisma

    async def create_infraction(self, infraction_type: InfractionType, infractor: Union[User, Member], target: Union[User, Member], reason: str) -> Infraction:
        table = await self.prisma.infraction.create(
            data={
                'type': infraction_type.value,
                'infractorid': infractor.id,
                'targetid': target.id,
                'reason': str(reason)
            }
        )
        return Infraction(table.id, infraction_type, infractor, target, reason)

    async def list_infractions(self, target: Union[Member, User],
                               infraction_type: Optional[InfractionType] = None) -> List[Infraction]:
        where_dict = {"targetid": target.id}
        if infraction_type:
            where_dict["type"] = infraction_type.value
        infractions = await self.prisma.infraction.find_many(
            where=where_dict,
            order={
                'created_at': 'asc'
            }
        )
        return [Infraction(infraction.id, InfractionType(infraction.type), self.client.get_user(infraction.infractorid),
                           target, infraction.reason) for infraction in infractions]

    # async def remove_infraction(self, infraction_type: InfractionType, target: Union[User, Member]) -> Infraction:
    #     pass




