import nextcord
import mizu.classes, mizu.utils


class DisboardAlert(mizu.classes.Base):
  def __init__(self, observer: mizu.utils.Hermes, disboard_id: int):
    self.observer = observer
    self.disboard_id = disboard_id

  async def check_bump(self, message: nextcord.Message):
    if message.author.id == self.disboard_id and message.embeds:
      if 'Bump done!' in message.embeds[0]:
        await self.alert_bump_done(message.author.id, message.guild.id)

  async def alert_bump_done(self, user_id, guild_id):
    await self.observer.async_notify(f'DBD-{guild_id}', [user_id, {'minutes': 1}])
