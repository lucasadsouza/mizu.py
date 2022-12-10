from __future__ import annotations

from nextcord.ext import commands
import mizu.classes, mizu.utils

class Pigeon(mizu.classes.Base):
  def __init__(self, bot: commands.Bot, db: mizu.utils.Koori):
    self.bot = bot
    self.db = db

  async def send(self, channel_id: int, message_code: str, language_code: str, replaceable: list[any]=[], user_id: int=None):
    if user_id:
      language_code = language_code

    message = self.db.get_message(message_code)

    channel = self.bot.get_channel(channel_id)
    await channel.send(message.get_message(language_code, replaceable))
