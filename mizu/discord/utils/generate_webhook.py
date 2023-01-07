import nextcord


async def generate_webhook(channel: nextcord.TextChannel, user: nextcord.User=None, name: str=None, avatar: bytes=None):
  for webhook in (await channel.webhooks()):
    if webhook.name == name or webhook.name == user.display_name:
      return webhook

  if user:
    return await channel.create_webhook(name=user.display_name, avatar=user.display_avatar)

  return await channel.create_webhook(name=name, avatar=avatar)
