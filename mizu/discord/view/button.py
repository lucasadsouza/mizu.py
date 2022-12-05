import nextcord, urllib.parse


class Button(nextcord.ui.View):
  def __init__(self, options: list[dict]):
    super().__init__()
    for option in options:
      self.add_item(nextcord.ui.Button(**option))


class URLButton(nextcord.ui.View):
  def __init__(self, options: list[dict]):
    super().__init__()
    for option in options:
      url = option['url'].split('?')
      try:
        url = f'{url[0]}?{urllib.parse.quote_plus(url[1])}'
      
      except IndexError:
        url = url[0]

      self.add_item(nextcord.ui.Button(label=option['label'], url=url))
