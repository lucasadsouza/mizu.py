class CheckPermissions():
  def __init__(self, db):
    self.db = db


  async def admin(self, member, channel, guild_id):
    if member.guild_permissions.administrator:
      return False

    await channel.send(self.db.get_message('CLN001', self.db.get_guild(guild_id, ['language'])))
    return True
