import datetime, math
import nextcord
from nextcord.ext import commands


class Pagination(nextcord.ui.View):
  def __init__(self, title: str=None, author: str=None, colour: int=None, type_: str='rich', url: str=None, description: str=None, timestamp: datetime.datetime=None, footer: str=None, image: str=None, thumbnail: str=None, fields_limit: int=5, bot: commands.Bot=None):
    super().__init__()
    self.value = None
  
    self.bot = bot
    self.embed_msg = None
    self.fields = []
    self.current_page = 1
    self.total_pages = 1

    self.embed = self.create_embed(title, colour, type_, url, description, timestamp)

    if author:
      self.embed.set_author(author)

    if footer:
      self.embed.set_footer(footer)
    
    if image:
      self.set_image(image)

    if thumbnail:
      self.set_thumbnail(thumbnail)


    if fields_limit <= 25:
      self.fields_limit = fields_limit
    
    else:
      self.fields_limit = 25

  def create_embed(self, title: str, colour: int, type_: str='rich', url: str=None, description: str=None, timestamp: datetime.datetime=None):
    embed = nextcord.Embed(colour=colour, title=title, type=type_, url=url, description=description, timestamp=timestamp)

    return embed

  def add_field(self, name: str, value: str, inline: bool=True):
    self.fields.append({'name': name, 'value': value, 'inline': inline})

    if len(self.fields) <= self.fields_limit:
      self.embed.add_field(name=name, value=value, inline=inline)

    self.total_pages = math.ceil(len(self.fields) / self.fields_limit)

  def add_fields(self, fields: list[dict]):
    for field in fields:
      self.add_field(**field)

  def turn_page(self):
    self.embed.clear_fields()

    for i in range((self.current_page - 1) * self.fields_limit, self.current_page * self.fields_limit):
      print(i)
      if i < len(self.fields):
        self.embed.add_field(**self.fields[i])

      else:
        break

  async def send(self, interaction: nextcord.Interaction):
    self.children[1].label = f'{self.current_page}/{self.total_pages}'

    self.embed_msg = await interaction.send(embed=self.embed, view=self)

  @nextcord.ui.button(emoji='<:arrow_back:1046879600703189032>', disabled=True)
  async def preview_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.current_page -= 1

    if self.current_page == 1:
      self.children[0].disabled = True

    if self.current_page < self.total_pages:
      self.children[2].disabled = False

    self.children[1].label = f'{self.current_page}/{self.total_pages}'
    
    self.turn_page()

    await self.embed_msg.edit(embed=self.embed, view=self)

  @nextcord.ui.button(label='0/1', disabled=True)
  async def page_label(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    pass

  @nextcord.ui.button(emoji='<:arrow_forward:1046879585297510481>')
  async def next_page(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.current_page += 1

    if self.current_page > 1:
      self.children[0].disabled = False

    if self.current_page == self.total_pages:
      self.children[2].disabled = True

    self.children[1].label = f'{self.current_page}/{self.total_pages}'

    self.turn_page()
    
    await self.embed_msg.edit(embed=self.embed, view=self)
