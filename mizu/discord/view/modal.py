import inspect

import nextcord, urllib.parse


class Modal(nextcord.ui.Modal):
  def __init__(self, title: str, options: list[dict], callback: callable=None):
    super().__init__(title)
    self.callback_func = callback

    for option in options:
      self.add_item(nextcord.ui.TextInput(**option))

  async def callback(self, interaction: nextcord.Interaction):
    self.values = [ child.value for child in self.children ]

    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.values)

    else:
      self.callback_func(interaction, self.values)
