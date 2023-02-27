from discord import Embed, Interaction, SelectOption
from discord.ui import Select
from lily.models.infractions import InfractionManager
from typing import List


class Remover(Select):

    def __init__(self, manager: InfractionManager, options: List[SelectOption]) -> None:
        self.infraction_manager = manager
        options = options

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a question to edit', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction) -> None:
        infraction_id = self.values[0]
        await self.infraction_manager.remove_infraction(infraction_id)
        await interaction.response.edit_message(content=f"Removed: {infraction_id}", embed=None, view=None)
