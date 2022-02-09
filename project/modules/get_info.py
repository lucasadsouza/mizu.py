from nextcord import Embed


class GetInfo():
  def __init__(self, db):
    self.db = db


  async def profile_picture(self, ctx, member):
    member_avatar = member.display_avatar.with_size(512)
    embed = Embed(title=member.display_name, description=self.db.get_message('GET001', self.db.get_guild(ctx.guild.id, ['language'])).replace('@url', member_avatar.url), colour=self.db.get_color('decimal', 'BlueGreen'))
    embed.set_image(url=member_avatar.url)

    await ctx.send(embed=embed)


  async def emoji(self, ctx, emoji):
    embed = Embed(title=f':{emoji.name}:', description=self.db.get_message('GET001', self.db.get_guild(ctx.guild.id, ['language'])).replace('@url', emoji.url), colour=self.db.get_color('decimal', 'BlueGreen'))
    embed.set_image(url=emoji.url)

    await ctx.send(embed=embed)
