from __future__ import annotations

import datetime, inspect
from nextcord.ext import commands, tasks
import mizu.utils
from mizu.classes import Base


class EventLoop(Base):
  def __init__(self, bot: commands.Bot, event: Event):
    self.bot = bot
    self.event = event

  @tasks.loop(hours=999, count=2)
  async def event_loop(self):
    self.event_loop.change_interval(seconds=self.event.get_remaining_time_in_seconds())

  # Send a message before the event_loop starts
  @event_loop.before_loop
  async def before_event_loop(self):
    await self.bot.wait_until_ready()

  # Stop the task to avoid problems and overflow
  @event_loop.after_loop
  async def after_event_loop(self):
    if not self.event_loop.is_being_cancelled():
      await self.event.stop()

  def run(self):
    self.event_loop.start()

  def stop(self):
    self.event_loop.stop()

  def is_running(self) -> bool:
    return self.event_loop.is_running()


class Event(Base):
  def __init__(self, bot: commands.Bot, observer: mizu.utils.Hermes, event_loop: EventLoop, guild_id: int, code: str, name: str, event_datetime: datetime.datetime, state: bool):
    self.bot = bot
    self.observer = observer
    self.event_loop = event_loop
    self.guild_id = guild_id
    self.code = code
    self.name = name
    self.datetime = event_datetime
    self.state = state

    self.is_running = False
    self.loop = None
    self.on_event_stop = None

  def __repr__(self):
    return f"<mizu.classes.Event code: '{self.code}', name: '{self.name}' guild_id: {self.guild_id}, datetime: {self.datetime}, state: {self.state}, is_running: {self.is_running}, loop: {self.loop}, on_event_stop: {self.on_event_stop}>"

  def update(self):
    self.observer.notify('update_Event', [self])

  def get_remaining_time_in_seconds(self) -> int:
    return round((self.datetime - datetime.datetime.now(datetime.timezone.utc)).total_seconds())

  def set_event_datetime(self, use_current_time: bool=True, days: int=0, hours: int=0, minutes: int=0, weeks: int=0):
    timedelta = datetime.timedelta(days=days, hours=hours, minutes=minutes, weeks=weeks)

    if use_current_time:
      self.datetime = datetime.datetime.now(datetime.timezone.utc) + timedelta

    else:
      self.datetime = self.datetime + timedelta

    if self.get_remaining_time_in_seconds() > 0:
      self.state = True
      self.run()

    self.update()

  def when_expires(self) -> int:
    return int(self.datetime.timestamp())

  def run(self):
    if not self.is_running and self.state:
      if self.get_remaining_time_in_seconds() > 0:
        self.loop = self.event_loop(self.bot, self)
        self.loop.run()

        self.is_running = True

      else:
        self.state = False
        self.update()

  async def stop(self):
    self.is_running = False
    self.state = False

    if self.loop and self.loop.is_running():
      self.loop.stop()

    if self.on_event_stop:
      if inspect.iscoroutinefunction(self.on_event_stop):
        await self.on_event_stop()

      else:
        self.on_event_stop()

    self.update()