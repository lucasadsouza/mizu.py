from __future__ import annotations

import nextcord
from nextcord.ext import commands
import mizu.classes, mizu.utils

class Pigeon(mizu.classes.Base):
  def __init__(self, bot: commands.Bot, db: mizu.utils.Koori):
    self.bot = bot
    self.db = db

  async def send(self, message_code: str, language: mizu.classes.Language, channel_id: int=None, interaction: nextcord.Interaction=None, embed: nextcord.Embed=None, view: nexcord.ui.view=None, file_: nextcord.File=None, replaceable: list[any]=[]):
    message = self.db.fetch_message(message_code)
    options = {}

    if embed:
      options['embed'] = embed
    
    if view:
      options['view'] = view

    if file_:
      options['file'] = file_

    if interaction:
      await interaction.send(message.get_message(language, replaceable), **options)

    elif channel_id:
      channel = self.bot.get_channel(channel_id)
      await channel.send(message.get_message(language, replaceable), **options)

  async def send_modal(self, interaction: nextcord.Interaction, modal: nextcord.ui.Modal):
    await interaction.response.send_modal(modal)
