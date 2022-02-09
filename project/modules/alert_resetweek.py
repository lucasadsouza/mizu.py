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

      # Starts the event
      self.event.run_event('DRW', use_current_time=True, days=6, hours=12)

    else:
      message = self.db.get_message('RSW002', int(self.db.get_constant('RESETWEEKLANG')))
      await ctx.reply(message)


  async def alert(self):
    resetweek_channel = int(self.db.get_constant('RESETWEEKCHANNEL'))
    resetweek_channel = self.bot.get_channel(resetweek_channel)
    resetweek_role = int(self.db.get_constant('RESETWEEKROLE'))

    message = self.db.get_message('RSW003', int(self.db.get_constant('RESETWEEKLANG')))

    await resetweek_channel.send(message.format(resetweek_role))
