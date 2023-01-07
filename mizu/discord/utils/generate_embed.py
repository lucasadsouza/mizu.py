import datetime
import nextcord


def generate_embed(color: nextcord.Colour or str=None, title: str=None, type: str='rich', url: str=None, description: str=None, timestamp: datetime.datetime=None, fields: list[dict]=[], author: dict=None, footer: dict=None, image_url: str=None, thumbnail_url: str=None):
  if color:
    color = nextcord.Colour.blurple()

  embed = nextcord.Embed(color=color, title=title, type=type, url=url, description=description, timestamp=timestamp)

  for field in fields:
    embed.add_field(**field)

  if author:
    embed.set_author(**author)

  if footer:
    embed.set_footer(**footer)

  if image_url:
    embed.set_image(image_url)

  if thumbnail_url:
    embed.set_thumbnail(thumbnail_url)   

  return embed
