from __future__ import annotations

import nextcord
import mizu.classes, mizu.discord.classes


class Member(mizu.classes.Base):
  def __init__(self, user: mizu.discord.classes.User, member_id: int, guild_id: int, discord_member: nextcord.Member):
    self.id = member_id
    self.guild_id = guild_id
    self.user = user
    self.raw = discord_member
