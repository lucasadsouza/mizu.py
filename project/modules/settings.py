from nextcord import Embed
import re


class Settings():
  def __init__(self, bot, db):
    self.bot = bot
    self.db = db


  def handle_channel_id(self, channel_id):
    try:
      return int(channel_id)

    except:
      return int((re.search('<#(.*)>', channel_id)).group(1))


  def handle_role_id(self, role_id):
    try:
      return int(role_id)

    except:
      return int((re.search('<@!(.*)>', role_id)).group(1))


  async def change_channel(self, ctx, channel_id, table, column, condition_column, condition_value, message_code):
    channel_id = self.handle_channel_id(channel_id)
    self.db.updateone(f'UPDATE {table} SET {column} = {channel_id} WHERE {condition_column} = {condition_value}')

    await ctx.send(self.db.get_message(message_code, self.db.get_guild(ctx.guild.id, ['language'])))


  async def change_role(self, ctx, role_id, table, column, condition_column, condition_value, message_code):
    role_id = self.handle_role_id(role_id)
    self.db.updateone(f'UPDATE {table} SET {column} = {role_id} WHERE {condition_column} = {condition_value}')

    await ctx.send(self.db.get_message(message_code, self.db.get_guild(ctx.guild.id, ['language'])))


  async def select_language(self, ctx):
    def check_reaction_user(reaction, user): # check if who is answering is the same that started the action
      return user == ctx.author

    guild_language = self.db.fetchone(f'SELECT code FROM language WHERE id = {self.db.get_guild(ctx.guild.id, ["language"])}')[0]
    languages = self.db.fetch(f'SELECT id, "name_{guild_language}" FROM language')

    description=''
    for lang in languages:
      description += f'{lang[0]} - {lang[1]}\n'
    embed = Embed(title=self.db.get_message('SET001', self.db.get_guild(ctx.guild.id, ['language'])), description=description, colour=self.db.get_color('decimal', 'LeadBlue'))

    embed = await ctx.send(embed=embed)

    reactions = ['0️⃣', '1️⃣', '2️⃣', '3️⃣']
    for reaction in reactions:
      await embed.add_reaction(reaction)

    reaction = (await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction_user))[0]

    await embed.delete()

    if str(reaction.emoji) == reactions[0]:
      return 0

    elif str(reaction.emoji) == reactions[1]:
      return 1

    elif str(reaction.emoji) == reactions[2]:
      return 2

    elif str(reaction.emoji) == reactions[3]:
      return 3




  async def resetweek_channel(self, ctx, channel_id):
    await self.change_channel(ctx, channel_id, 'constant', 'constant', 'name', '"RESETWEEKCHANNEL"', 'SET002')


  async def resetweek_role(self, ctx, role_id):
    await self.change_role(ctx, role_id, 'constant', 'constant', 'name', '"RESETWEEKROLE"', 'SET003')


  async def resetweek_language(self, ctx):
    language = await self.select_language(ctx)
    self.db.updateone(f'UPDATE constant SET constant = {language} WHERE name = "RESETWEEKLANG"')

    await ctx.send(self.db.get_message('SET004', self.db.get_guild(ctx.guild.id, ['language'])))




  async def daily_mizucoins(self, ctx, time):
    self.db.updateone(f'UPDATE event SET datetime = {time} WHERE code = "DMC"')

    await ctx.send(self.db.get_message('SET005', self.db.get_guild(ctx.guild.id, ['language'])))




  async def guild_id(self, guild_id, new_id):
    self.db.updateone(f'UPDATE guild SET guild_id = {new_id} WHERE guild_id = {guild_id}')

    await ctx.send(self.db.get_message('SET006', self.db.get_guild(ctx.guild.id, ['language'])))


  async def guild_language(self, ctx, language):
    language = await self.select_language(ctx)

    self.db.updateone(f'UPDATE guild SET language = {language} WHERE guild_id = {ctx.guild.id}')

    await ctx.send(self.db.get_message('SET007', self.db.get_guild(ctx.guild.id, ['language'])))


  async def guild_log_channel(self, ctx, channel_id):
    await self.change_channel(ctx, channel_id, 'guild', 'log_channel', 'guild_id', ctx.guild.id, 'SET008')


  async def guild_sync_channel(self, ctx, channel_id):
    await self.change_channel(ctx, channel_id, 'guild', 'sync_channel', 'guild_id', ctx.guild.id, 'SET009')


  async def guild_disboard_channel(self, ctx, channel_id):
    await self.change_channel(ctx, channel_id, 'guild', 'disboard_channel', 'guild_id', ctx.guild.id, 'SET010')


  async def guild_disboard_role(self, ctx, disboard_role_id):
    await self.change_role(ctx, role_id, 'guild', 'disboard_role', 'guild_id', ctx.guild.id, 'SET011')


  async def guild_welcome_channel(self, ctx, channel_id):
    await self.change_channel(ctx, channel_id, 'guild', 'welcome_channel', 'guild_id', ctx.guild.id, 'SET012')


  async def guild_welcome_background(self, ctx, background_image):
    self.db.updateone(f'UPDATE image SET image = {background_image} WHERE guild_id = {ctx.guild.id}')

    await ctx.send(self.db.get_message('SET013', self.db.get_guild(ctx.guild.id, ['language'])))
