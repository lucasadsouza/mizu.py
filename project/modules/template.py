from discord import Embed


# Handle guild's template
class Template():
  def __init__(self, bot, db, checkpermissions):
    self.bot = bot
    self.db = db
    self.checkpermissions = checkpermissions


  # Create a guild template
  async def new(self, ctx, name, description):
    if await self.checkpermissions.admin(ctx.author, ctx.channel, ctx.guild.id):
      return False

    def check_user(msg): # check if who is answering is the same that started the action
      return msg.author == ctx.author

    if len(name) < 1 or len(name) > 100:
      return False


    if description == '-no':
      description = None

    else:
      if description == None:
        await ctx.send(self.db.get_message('TPT001', self.db.get_guild(ctx.guild.id, ['language'])).format(name))

        description = (await self.bot.wait_for('message', timeout=60.0, check=check_user)).content
        if description == '-no':
          description = None

    template = await ctx.guild.create_template(name=name, description=description)

    await ctx.send(self.db.get_message('TPT002', self.db.get_guild(ctx.guild.id, ['language'])).format(template.name))


  # Show a guild template
  async def show(self, ctx):
    if await self.checkpermissions.admin(ctx.author, ctx.channel, ctx.guild.id):
      return False

    template = (await ctx.guild.templates())[0]


    if template.description == None:
      embed = Embed(title=template.name, description=self.db.get_message('TPT003', self.db.get_guild(ctx.guild.id, ['language'])), colour=self.db.get_color('decimal', 'LeadBlue'))

    else:
      embed = Embed(title=template.name, description=template.description, colour=self.db.get_color('decimal', 'LeadBlue'))

    embed.add_field(name=self.db.get_message('TPT004', self.db.get_guild(ctx.guild.id, ['language'])), value=template.creator.name, inline=False)
    embed.add_field(name=self.db.get_message('TPT005', self.db.get_guild(ctx.guild.id, ['language'])), value=template.code, inline=False)
    embed.add_field(name=self.db.get_message('TPT006', self.db.get_guild(ctx.guild.id, ['language'])), value=template.uses, inline=False)
    embed.add_field(name=self.db.get_message('TPT007', self.db.get_guild(ctx.guild.id, ['language'])), value=template.source_guild.name, inline=False)

    await ctx.send(embed=embed)


  # Syncronize a guild template
  async def sync(self, ctx):
    if await self.checkpermissions.admin(ctx.author, ctx.channel, ctx.guild.id):
      return False

    template = (await ctx.guild.templates())[0]

    await template.sync()

    await ctx.send(self.db.get_message('TPT008', self.db.get_guild(ctx.guild.id, ['language'])).format(template.name))


  # Edit a guild template
  async def edit(self, ctx):
    if await self.checkpermissions.admin(ctx.author, ctx.channel, ctx.guild.id):
      return False

    def check_user(msg): # check if who is answering is the same that started the action
      return msg.author == ctx.author


    template = (await ctx.guild.templates())[0]
    await ctx.send(self.db.get_message('TPT009', self.db.get_guild(ctx.guild.id, ['language'])).format(template.name))

    await ctx.send(self.db.get_message('TPT010', self.db.get_guild(ctx.guild.id, ['language'])))
    name = (await self.bot.wait_for('message', timeout=60.0, check=check_user)).content

    if name == '-no':
      name = template.name


    await ctx.send(self.db.get_message('TPT011', self.db.get_guild(ctx.guild.id, ['language'])))
    description = (await self.bot.wait_for('message', timeout=60.0, check=check_user)).content

    if description == '-no':
      description = template.description

    await template.edit(name=name, description=description)

    await ctx.send(self.db.get_message('TPT012', self.db.get_guild(ctx.guild.id, ['language'])))


  # Delete a guild template
  async def delete(self, ctx):
    if await self.checkpermissions.admin(ctx.author, ctx.channel, ctx.guild.id):
      return False

    template = (await ctx.guild.templates())[0]
    template_name = template.name
    await template.delete()

    await ctx.send(self.db.get_message('TPT013', self.db.get_guild(ctx.guild.id, ['language'])).format(template_name))
