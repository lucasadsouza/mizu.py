from nextcord.ext import tasks




# Alert to reset the week on Discloud
class AlertResetWeek():
  def __init__(self, bot, db, event):
    self.bot = bot
    self.db = db
    self.event = event


  # Check if week was reseted
  async def reseted(self, ctx):
    if ctx.author.id == 541033481199812628:

      resetweek_channel = int(self.db.get_constant('RESETWEEKCHANNEL'))
      resetweek_channel = self.bot.get_channel(resetweek_channel)

      message = self.db.get_message('RSW001', int(self.db.get_constant('RESETWEEKLANG')))

      await resetweek_channel.send(message)

      # Starts the alert
      # resetWeekLoop = ResetWeekLoop(self.bot, self.db)
      self.event.run_event('DRW', use_current_time=True, days=7)

    else:
      message = self.db.get_message('RSW002', int(self.db.get_constant('RESETWEEKLANG')))
      await ctx.reply(message)


  async def alert(self):
    resetweek_channel = int(self.db.get_constant('RESETWEEKCHANNEL'))
    resetweek_channel = self.bot.get_channel(resetweek_channel)
    resetweek_role = int(self.db.get_constant('RESETWEEKROLE'))

    message = self.db.get_message('RSW003', int(self.db.get_constant('RESETWEEKLANG')))

    await resetweek_channel.send(message.format(resetweek_role))




# One time loop that starts when the week is reseted to alert when reset again
class ResetWeekLoop():
  def __init__(self, bot, db):
    self.bot = bot
    self.db = db

    self.resetweek_alert.start()


  @tasks.loop (hours=167, count=2)
  async def resetweek_alert(self):
    # Skip the loop at the start
    if self.resetweek_alert.current_loop != 0:
      resetweek_channel = int(self.db.get_constant('RESETWEEKCHANNEL'))
      resetweek_channel = self.bot.get_channel(resetweek_channel)
      resetweek_role = int(self.db.get_constant('RESETWEEKROLE'))

      message = self.db.get_message('RSW003', int(self.db.get_constant('RESETWEEKLANG')))

      await resetweek_channel.send(message.format(resetweek_role))


  # Send a message before the resetweek_alert starts
  @resetweek_alert.before_loop
  async def before_resetweek_alert(self):
    await self.bot.wait_until_ready()
    print('started')


  # Stop the task to avoid problems and overflow
  @resetweek_alert.after_loop
  async def after_resetweek_alert(self):
    self.resetweek_alert.stop()
