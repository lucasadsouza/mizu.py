import mizu.discord.classes


def member_factory(params: list[any]=[]) -> mizu.discord.classes.Member:
  member = mizu.discord.classes.Member(*params)

  return member
