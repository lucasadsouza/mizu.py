from nextcord.ext import tasks

from datetime import datetime, timedelta, timezone



class Event():
  def __init__(self, bot, db):
    self.bot = bot
    self.db = db


  def event_time(self, event_code):
    event = self.db.get_event(event_code)[1]
    now = datetime.now(timezone.utc)

    event_time = event - now

    event_in_hours = event_time.total_seconds() / 3600

    return event_in_hours


  def run_events(self, events):
    for event in events:
      event_time = self.event_time(event)
      if event_time > 0:
        eventLoop = EventLoop(self.bot, self.db, event, event_time)


  def run_event(self, event_code, use_current_time=False, days=0, hours=0, minutes=0):
    if use_current_time:
      date_time = datetime.now(timezone.utc) + timedelta(days=days, hours=hours, minutes=minutes)

    else:
      date_time = self.db.get_event(event_code)[1] + timedelta(days=days, hours=hours, minutes=minutes)

    self.db.set_event_datetime(event_code, date_time)

    eventLoop = EventLoop(self.bot, self.db, event_code, self.event_time(event_code))



class EventLoop():
  def __init__(self, bot, db, event_code, event_hours):
    self.bot = bot
    self.db = db
    self.event_code = event_code
    self.event_hours = event_hours

    self.event_alert.start()


  @tasks.loop(hours=999, count=2)
  async def event_alert(self):
    self.event_alert.change_interval(hours=self.event_hours)
    # Skip the loop at the start
    if self.event_alert.current_loop != 0:
      print(f'end ({self.event_code}): {datetime.now(timezone.utc)}')
      self.db.change_event_state(self.event_code)
      print(f'{self.event_code}: Event now!!!!')


  # Send a message before the event_alert starts
  @event_alert.before_loop
  async def before_event_alert(self):
    await self.bot.wait_until_ready()
    print(f'{self.event_code}: {self.event_hours * 60} mins')
    print(f'start ({self.event_code}): {datetime.now(timezone.utc)}')


  # Stop the task to avoid problems and overflow
  @event_alert.after_loop
  async def after_event_alert(self):
    self.event_alert.stop()
