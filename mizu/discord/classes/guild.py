from __future__ import annotations

import os
import nextcord
import mizu.classes, mizu.utils


class Guild(mizu.classes.Base):
  def __init__(self, observer: mizu.utils.Hermes, guild_id: int, discord_guild: nextcord.Guild, language: mizu.classes.Language, log_channel: int, sync_channel: int, disboard_channel: int, disboard_role: str, welcome_channel: int, welcome_message: str, welcome_image: mizu.classes.Image):
    self.observer = observer
    self.id = guild_id
    self.raw = discord_guild
    self.language = language
    self.log_channel = log_channel
    self.sync_channel = sync_channel
    self.disboard_channel = disboard_channel
    self.disboard_role = disboard_role
    self.welcome_channel = welcome_channel
    self.welcome_message = welcome_message
    self.welcome_image = welcome_image
    self.events = {}
    self.members = {}
    self.temp_path = 'temp'

  def update(self):
    self.observer.notify('update_Guild', [self])

  def add_event(self, event: Event):
    if event.code == 'DBA':
      event.on_event_stop = self.alert_to_bump

    self.events[event.code] = event

  def add_member(self, member: Member):
    self.members[member.id] = member

  def set_language(self, language: mizu.classes.Language):
    self.language = language

    self.update()

  def set_channel(self, type: str, id_: int):
    if type == 'log':
      self.log_channel = id_
    
    if type == 'sync':
      self.sync_channel = id_

    if type == 'disboard':
      self.sync_channel = id_
    
    if type == 'welcome':
      self.welcome_channel = id_

    self.update()

  def set_disboard_role(self, role: str):
    self.disboard_role = role

    self.update()

  def set_welcome_message(self, message: str):
    self.welcome_message = message

    self.update()

  def load_welcome_image(self) -> str:
    if not os.path.exists(self.temp_path):
      os.mkdir(self.temp_path)

    # Saves background image on temp directory
    path = os.path.join(self.temp_path, 'guild_background.jpg')
    with open(path, 'wb') as file:
      file.write(self.welcome_image)

    return path

  def run_events(self):
    for event in self.events.values():
      event.run()

  async def when_bump_done(self, user_id, restart_time: int):
    self.events['DBA'].set_event_datetime(True, **restart_time)
    await self.observer.async_notify('send_Pigeon', [self.disboard_channel, 'DSB001', self.members[user_id].user.language.code, [], user_id])
    await self.observer.async_notify('send_Pigeon', [self.disboard_channel, 'DSB003', self.language.code, [self.events['DBA'].when_expires()]])

  async def alert_to_bump(self):
    await self.observer.async_notify('send_Pigeon', [self.disboard_channel, 'DSB002', self.language.code, [self.disboard_role]])
