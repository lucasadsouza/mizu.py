from nextcord.ext import tasks
import re




# Checks if Disboard was bumped and start an alert to bump again
class CheckDisboard():
  def __init__(self, bot, db):
    self.bot = bot
    self.db = db


  # Gets the user that bumped
  def get_user(self, msg):
    return int((re.search('<@(.*)>', msg.embeds[0].description)).group(1))


  # Check if the bump was done
  async def bumped(self, msg):
    if msg.author.id == 302050872383242240 and msg.embeds and 'Bump done!' in msg.embeds[0].description:
      user = self.get_user(msg)

      disboard_settings = self.db.get_guild(msg.guild.id, ['disboard_channel', 'language'])
      disboard_channel = self.bot.get_channel(disboard_settings[0])
      message = self.db.get_message('DSB001', disboard_settings[1])

      await disboard_channel.send(message.format(user))

      # Starts the alert
      disboardLoop = DisboardLoop(self.bot, self.db, msg.guild.id)




# One time loop that starts when a bump is done on Disboard to alert when bump again
class DisboardLoop():
  def __init__(self, bot, db, guild_id):
    self.bot = bot
    self.db = db
    self.guild_id = guild_id

    self.disboard_alert.start()


  @tasks.loop(hours=2, count=2)
  async def disboard_alert(self):
    # Skip the loop at the start
    if self.disboard_alert.current_loop != 0:
      disboard_settings = self.db.get_guild(self.guild_id, ['disboard_channel', 'language'])
      disboard_channel = self.bot.get_channel(disboard_settings[0])
      message = self.db.get_message('DSB002', disboard_settings[1])
      disboard_role = self.db.get_guild(self.guild_id, ["disboard_role"])

      await disboard_channel.send(message.format(disboard_role))


  # Send a message before the disboard_alert starts
  @disboard_alert.before_loop
  async def before_disboard_alert(self):
    await self.bot.wait_until_ready()
    print('started')


  # Stop the task to avoid problems and overflow
  @disboard_alert.after_loop
  async def after_disboard_alert(self):
    self.disboard_alert.stop()
