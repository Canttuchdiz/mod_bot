from discord import SelectOption
from discord.ui import View
from lily.models.selects import Remover
from lily.models.infractions import InfractionManager
from typing import List


class InfractionRemove(View):

    def __init__(self, manager: InfractionManager, options: List[SelectOption]) -> None:
        super().__init__(timeout=None)
        self.manager = manager
        self.options = options
        self.select = Remover(self.manager, self.options)
        self.add_item(self.select)
