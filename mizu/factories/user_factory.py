import mizu.discord.classes


def user_factory(params: list[any]=[]) -> mizu.discord.classes.User:
  user = mizu.discord.classes.User(*params)

  return user
