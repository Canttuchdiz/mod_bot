from discord import Embed, Color


class UtilMethods:

    @staticmethod
    async def embedify(title: str, description: str, color: Color) -> Embed:
        embed = Embed(title=title, description=description, color=color)
        return embed
