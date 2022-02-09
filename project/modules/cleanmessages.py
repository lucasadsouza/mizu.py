import re


# Deletes messages
class Clean():
  def __init__(self, db):
    self.db = db


  async def validate(self, ctx, range):
    if ctx.author.guild_permissions.administrator == False:
      await ctx.send(self.db.get_message('CLN001', self.db.get_guild(ctx.guild.id, ['language'])))
      return False

    if range == 0:
      await ctx.send(self.db.get_message('CLN005', self.db.get_guild(ctx.guild.id, ['language'])))
      return False


  # Manage to send personalized logs about the deleted messages
  def logs(self, guild_id, history_list):
    guild_language = self.db.get_guild(guild_id, ['language'])
    if len(history_list) - 1 == 0:
      return self.db.get_message('CLN002', guild_language)

    elif len(history_list) - 1 == 1:
      return self.db.get_message('CLN003', guild_language)

    else:
      return self.db.get_message('CLN004', guild_language).format(len(history_list) - 1)


  # Deletes a range of messages
  async def clean(self, ctx, range):
    if self.validate(ctx, range) == False:
      return False

    history = ctx.channel.history(limit=int(range) + 1)
    history_list = [x async for x in history]

    await ctx.channel.delete_messages(history_list)

    await ctx.send(self.logs(ctx.guild.id, history_list))


  async def clean_from(self, ctx, range, from_):
    if self.validate(ctx, range) == False:
      return False

    history = ctx.channel.history(limit=int(range) + 1)
    history_list = []

    async for msg in history:
      if int(msg.author.id) == int((re.search('<@!(.*)>', from_)).group(1)):
        history_list.append(msg)

    await ctx.channel.delete_messages(history_list)

    await ctx.send(self.logs(ctx.guild.id, history_list))




# class Clean ():
#   async def clean_from (self, ctx, range, from_):
#     if ctx.author.guild_permissions.administrator:
#       history = ctx.channel.history(limit=(int(range) + 1))
#       self.historyList = []

#       async for msg in history:
#         if int(msg.author.id) == int((re.search('<@!(.*)>', from_)).group(1)):
#           self.historyList.append(msg)

#       await ctx.channel.delete_messages(self.historyList)

#       self.log(ctx.guild.id)
