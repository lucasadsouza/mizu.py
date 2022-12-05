import inspect
import nextcord


class StringDropdown(nextcord.ui.StringSelect):
  def __init__(self, options: list[dict], placeholder: str='', min_value: int=1, max_value: int=1, callback: callable=None):
    self.callback_func = callback
    view_options = []
    for option in options:
      view_options.append(nextcord.SelectOption(**option))

      super().__init__(placeholder=placeholder, min_values=min_value, max_values=max_value, options=view_options)

  async def callback(self, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.values)

    else:
      self.callback_func(interaction, self.values)


class ChannelDropdown(nextcord.ui.ChannelSelect):
  def __init__(self, placeholder: str='', min_value: int=1, max_value: int=1, callback: callable=None, channel_type: list[nextcord.ChannelType]=None):
    self.callback_func = callback

    super().__init__(placeholder=placeholder, min_values=min_value, max_values=max_value, channel_types=channel_type)

  async def callback(self, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.values)

    else:
      self.callback_func(interaction, self.values)


class RoleDropdown(nextcord.ui.RoleSelect):
  def __init__(self, placeholder: str='', min_value: int=1, max_value: int=1, callback: callable=None):
    self.callback_func = callback

    super().__init__(placeholder=placeholder, min_values=min_value, max_values=max_value)

  async def callback(self, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.values)

    else:
      self.callback_func(interaction, self.values)


class UserDropdown(nextcord.ui.UserSelect):
  def __init__(self, placeholder: str='', min_value: int=1, max_value: int=1, callback: callable=None):
    self.callback_func = callback

    super().__init__(placeholder=placeholder, min_values=min_value, max_values=max_value)

  async def callback(self, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.values)

    else:
      self.callback_func(interaction, self.values)


class MentionableDropdown(nextcord.ui.MentionableSelect):
  def __init__(self, placeholder: str='', min_value: int=1, max_value: int=1, callback: callable=None):
    self.callback_func = callback

    super().__init__(placeholder=placeholder, min_values=min_value, max_values=max_value)

  async def callback(self, interaction: nextcord.Interaction):
    if inspect.iscoroutinefunction(self.callback_func):
      await self.callback_func(interaction, self.values)

    else:
      self.callback_func(interaction, self.values)


class Dropdown(nextcord.ui.View):
    def __init__(self, type: str='default', placeholder: str='', min_value: int=1, max_value: int=1, callback: callable=None, options: list[dict]=None, channel_type: list[nextcord.ChannelType]=None):
        super().__init__()
        if type == 'default':
          self.add_item(StringDropdown(options, placeholder, min_value, max_value, callback))

        elif type == 'channel':
          self.add_item(ChannelDropdown(placeholder, min_value, max_value, callback, channel_type))

        elif type == 'role':
          self.add_item(RoleDropdown(placeholder, min_value, max_value, callback))

        elif type == 'user':
          self.add_item(UserDropdown(placeholder, min_value, max_value, callback))

        elif type == 'mentionable':
          self.add_item(MentionableDropdown(placeholder, min_value, max_value, callback))