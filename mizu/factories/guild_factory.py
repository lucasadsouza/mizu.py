import mizu.classes, mizu.discord.classes


def guild_factory(params:list[any]=[], events: list[mizu.classes.Event]=[], members: list[mizu.discord.classes.Member]=[]) -> mizu.discord.classes.Guild:
  guild = mizu.discord.classes.Guild(*params)

  for event in events:
    guild.add_event(event)

  for member in members:
    guild.add_member(member)

  return guild
