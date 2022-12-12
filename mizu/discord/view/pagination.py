import datetime, math, inspect
import nextcord
from nextcord.ext import commands


class Pagination(nextcord.ui.View):
  def __init__(self, title: str=None, author: str=None, colour: int=None, type_: str='rich', url: str=None, description: str=None, timestamp: datetime.datetime=None, footer: str=None, thumbnail: str=None, fields_limit: int=5, bot: commands.Bot=None):
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

  @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:done:1051614776922484836>')
  async def select_image(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.current_page - 1)

    else:
      self.callback_func(interaction, self.current_page - 1)


class ImagePagination(nextcord.ui.View):
  def __init__(self, title: str=None, author: str=None, colour: int=None, type_: str='rich', url: str=None, description: str=None, timestamp: datetime.datetime=None, footer: str=None, thumbnail: str=None, images_limit: int=5, bot: commands.Bot=None, callback_func: callable=None):
    super().__init__()
    self.value = None
  
    self.bot = bot
    self.embed_msg = None
    self.images = []
    self.current_page = 1
    self.total_pages = 1
    self.images_limit = images_limit
    self.callback_func = callback_func

    self.embed = self.create_embed(title, colour, type_, url, description, timestamp)

    if author:
      self.embed.set_author(author)

    if footer:
      self.embed.set_footer(footer)

    if thumbnail:
      self.set_thumbnail(thumbnail)

  def create_embed(self, title: str, colour: int, type_: str='rich', url: str=None, description: str=None, timestamp: datetime.datetime=None):
    embed = nextcord.Embed(colour=colour, title=title, type=type_, url=url, description=description, timestamp=timestamp)

    return embed

  def add_image(self, url: str):
    self.images.append(url)

    if len(self.images) == 1:
      self.embed.set_image(url)

    self.total_pages = len(self.images)

  def turn_page(self):
    self.embed.set_image(self.images[self.current_page - 1])

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

  @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji='<:done:1051614776922484836>')
  async def select_image(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.current_page - 1)

    else:
      self.callback_func(interaction, self.current_page - 1)
