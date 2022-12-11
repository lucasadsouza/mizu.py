from __future__ import annotations

import datetime
from nextcord.ext import commands
import dbtools
import mizu.classes, mizu.utils, mizu.factories, mizu.exceptions


qb = dbtools.querybuilder.SQLQueryBuilder()

class KooriCache(mizu.classes.Base):
  def __init__(self, size: int=5):
    self.languages = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.constants = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.colors = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.messages = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.log_messages = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.error_messages = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.users = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.members = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.events = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.guilds = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)
    self.images = mizu.utils.Stack(use_deque=True, max_size=size, discard=True)


class Koori(dbtools.databases.SQLiteDB):
  def __init__(self, database_path: str, bot: commands.Bot, observer: mizu.utils.Hermes=None):
    super().__init__(database_path)

    self.bot = bot
    self.observer = observer
    self.cached = KooriCache(15)
    self.errorraiser = mizu.exceptions.ErrorRaiser(self, self.fetch_constant('LOGLANGUAGE'))

  def fetch_constant(self, name: str) -> str:
    if not self.exists('constant', name=name):
      self.errorraiser.raise_error('constant', 'KOO001')

    try:
      return self.cached.constants.search('name', name)['value']

    except IndexError:
      response = self.fetchone(qb.SELECT('value', 'type').FROM('constant').WHERE(qb.EQUALS('name', name)).get_query())
  
      if response[1] == 'int':
        response = int(response[0])

      elif response[1] == 'float':
        response = float(response[0])

      elif response[1] == 'bool':
        response = bool(int(response[0]))

      elif response[1] == 'Language':
        response = self.fetch_language(response[0])

      else:
        response = response[0]

      self.cached.constants.push({'name': name, 'value': response})

      return response

  def fetch_color(self, name: str) -> mizu.classes.Color:
    if not self.exists('color', name=name):
      self.errorraiser.raise_error('color', 'KOO002')

    try:
      return self.cached.colors.search('name', name)['value']

    except IndexError:
      response = self.fetchone(qb.SELECT(qb.ALL).FROM('color').WHERE(qb.EQUALS('name', name)).get_query())
      color = mizu.classes.Color(response[0], response[1])

      self.cached.constants.push({'name': name, 'value': color})

      return color

  def fetch_language(self, code: str) -> mizu.classes.Language:
    if not self.exists('language', code=code):
      self.errorraiser.raise_error('language', 'KOO003')

    try:
      return self.cached.languages.search('code', code)['value']

    except IndexError:
      response = self.fetchone(qb.SELECT(qb.ALL).FROM('language').WHERE(qb.EQUALS('code', code)).get_query())
      columns = self.fetch(qb.SELECT('name').FROM(qb.PRAGMA_TABLE_INFO('language')).get_query())

      labels = []
      for column_name, label in zip(columns[1:], response[1:]):
        labels.append((column_name[0], label))

      language = mizu.factories.language_factory([self, response[0]], [*labels])
      self.cached.languages.push({'code': code, 'value': language})

      return language

  def fetch_available_languages(self, code: str=None, labels: bool=True) -> list:
    if not self.exists('language', code=code):
      self.errorraiser.raise_error('language', 'KOO003')

    if labels:
      return self.fetch(qb.SELECT('code', code).FROM('language').get_query())

    return sself.fetch(qb.SELECT('code').FROM('language').get_query())

  def fetch_message(self, code: str) -> mizu.classes.Message:
    if not self.exists('message', code=code):
      self.errorraiser.raise_error('message', 'KOO004')

    try:
      return self.cached.messages.search('code', code)['value']

    except IndexError:
      response = self.fetch(qb.SELECT(qb.ALL).FROM('message').WHERE(qb.EQUALS('code', code)).get_query())

      message = mizu.classes.Message(self, code)
      for item in response:
        message.add_message(item[1], item[2])

      self.cached.messages.push({'code': code, 'value': message})

      return message

  def fetch_log_message(self, code: str) -> mizu.classes.LogMessage:
    if not self.exists('log_message', code=code):
      self.errorraiser.raise_error('message', 'KOO005')

    try:
      return self.cached.log_messages.search('code', code)['value']

    except IndexError:
      response = self.fetch(qb.SELECT(qb.ALL).FROM('log_message').WHERE(qb.EQUALS('code', code)).get_query())

      log_message = mizu.classes.LogMessage(self, code)
      for item in response:
        log_message.add_message(item[1], item[2])

      self.cached.log_messages.push({'code': code, 'value': log_message})

      return log_message

  def fetch_error_message(self, code: str) -> mizu.classes.ErrorMessage:
    if not self.exists('error_message', code=code):
      self.errorraiser.raise_error('message', 'KOO006')

    try:
      return self.cached.error_messages.search('code', code)['value']

    except IndexError:
      response = self.fetch(qb.SELECT(qb.ALL).FROM('error_message').WHERE(qb.EQUALS('code', code)).get_query())

      error_message = mizu.classes.ErrorMessage(self, code)
      for item in response:
        error_message.add_message(item[1], item[2])

      self.cached.error_messages.push({'code': code, 'value': error_message})

      return error_message

  async def fetch_user(self, id_: int) -> mizu.classes.User:
    if not self.exists('user', id=id_):
      self.errorraiser.raise_error('user', 'KOO007')

    try:
      return self.cached.users.search('id', id_)['value']

    except IndexError:
      response = self.fetchone(qb.SELECT(qb.ALL).FROM('user').WHERE(qb.EQUALS('id', id_)).get_query())
      raw_user = await self.bot.fetch_user(id_)

      user = mizu.factories.user_factory([self.observer, response[0], raw_user, self.fetch_language(response[1]), *response[2:4], response[4]])

      self.cached.users.push({'id': id_, 'value': user})

      return user

  async def fetch_member(self, id_: int) -> mizu.classes.Member:
    if not self.exists('member', id=id_):
      self.errorraiser.raise_error('member', 'KOO008')

    try:
      return self.cached.members.search('id', id_)['value']

    except IndexError:
      response = self.fetchone(qb.SELECT(qb.ALL).FROM('member').WHERE(qb.EQUALS('id', id_)).get_query())
      guild = await self.bot.fetch_guild(response[1])

      member = mizu.factories.member_factory([await self.fetch_user(response[0]), *response[:2], await guild.fetch_member(response[0])])

      self.cached.members.push({'id': id_, 'value': member})

      return member

  def fetch_event(self, code: str, guild_id: int) -> mizu.classes.Event:
    if not self.exists('event', guild_id=guild_id, code=code):
      self.errorraiser.raise_error('event', 'KOO009')

    try:
      return self.cached.events.search('code_id', f'{code}-{guild_id}')['value']

    except IndexError:
      response = self.fetchone(qb.SELECT(qb.ALL).FROM('event').WHERE(qb.EQUALS('guild_id', guild_id), qb.AND, qb.EQUALS('code', code)).get_query())

      event = mizu.factories.event_factory([self.bot, self.observer, mizu.classes.EventLoop, *response[:4], response[4]])

      self.cached.events.push({'code_id': f'{code}-{guild_id}', 'value': event})

    return event

  async def fetch_guild(self, id_: int) -> mizu.classes.Guild:
    if not self.exists('guild', id=id_):
      self.errorraiser.raise_error('guild', 'KOO010')

    try:
      return self.cached.guilds.search('id', id_)['value']

    except IndexError:
      response = self.fetchone(qb.SELECT(qb.ALL).FROM('guild').WHERE(qb.EQUALS('id', id_)).get_query())
      events = self.fetch(qb.SELECT(qb.ALL).FROM('event').WHERE(qb.EQUALS('guild_id', id_)).get_query())
      members = self.fetch(qb.SELECT('id').FROM('member').WHERE(qb.EQUALS('guild_id', id_)).get_query())
      raw_guild = await self.bot.fetch_guild(id_)
    
      events_list = [ self.fetch_event(event[1], event[0]) for event in events ]
      members_list = [ await self.fetch_member(member[0]) for member in members ]
      background_img = self.fetch_welcome_image(id_)

      guild = mizu.factories.guild_factory([self.observer, id_, raw_guild, self.fetch_language(response[1]), *response[2:], background_img], events_list, members_list)
  
      self.cached.guilds.push({'id': id_, 'value': guild})

      return guild

  def fetch_image(self, id_: int) -> mizu.classes.Image:
    if not self.exists('image', id=id_):
      self.errorraiser.raise_error('image', 'KOO015')

    try:
      return self.cached.images.search('id', id_)['value']

    except IndexError:
      image = self.fetchone(qb.SELECT('image').FROM('image').WHERE(qb.EQUALS('id', id_)).get_query())[0]
      image = mizu.classes.Image(image)

      self.cached.images.push({'id': id_, 'value': image})

      return image

  def fetch_welcome_image(self, id_: int) -> mizu.classes.Image:
    if not self.exists('welcome_image', id=id_):
      self.errorraiser.raise_error('image', 'KOO015')

    try:
      return self.cached.images.search('id', id_)['value']

    except IndexError:
      image = self.fetchone(qb.SELECT('image').FROM('welcome_image').WHERE(qb.EQUALS('id', id_)).get_query())[0]
      image = mizu.classes.Image(image)

      self.cached.images.push({'id': id_, 'value': image})

      return image

  def insert_guild(self, guild: nextcord.Guild):
    if self.exists('guild', id=guild.id):
      self.errorraiser.raise_error('guild', 'KOO011')
    
    if guild.preferred_locale in [ code[0] for code in self.fetch_available_languages(label=False) ]:
      self.insert(qb.INSERT_INTO('guild', ['id', 'language']).VALUES(guild.id, guild.preferred_locale).get_query())

    else:
      self.insert(qb.INSERT_INTO('guild', ['id']).VALUES(guild.id).get_query())

    background_img = self.fetch_image(0)
    self.insert_welcome_image(id_, background_img)

  def insert_user(self, id_: int, language_code: str):
    if self.exists('user', id=id_):
      self.errorraiser.raise_error('member', 'KOO012')

    self.insert(qb.INSERT_INTO('user', ['id', 'language']).VALUES(id_, language_code))

  def insert_member(self, id_: int, guild_id: int):
    if self.exists('member', id=id_):
      self.errorraiser.raise_error('member', 'KOO013')

    self.insert(qb.INSERT_INTO('member', ['id', 'guild_id']).VALUES(id_, guild_id))

  def insert_image(self, id_: int, image: bytes):
    if self.exists('image', id=id_):
      self.errorraiser.raise_error('image', 'KOO014')

    self.insert(qb.INSERT_INTO('image').VALUES(id_, image).get_query())

  def insert_welcome_image(self, id_: int, image: bytes):
    if self.exists('welcome_image', id=id_):
      self.errorraiser.raise_error('image', 'KOO014')

    self.insert(qb.INSERT_INTO('welcome_image').VALUES(id_, image).get_query())

  def update_guild(self, guild: mizu.classes.Guild):
    if not self.exists('guild', id=guild.id):
      self.errorraiser.raise_error('guild', 'KOO010')

    self.update(qb.UPDATE('guild').SET(
      language=guild.language.code,
      log_channel=guild.log_channel,
      sync_channel=guild.sync_channel,
      disboard_channel=guild.disboard_channel,
      disboard_role=guild.disboard_role,
      welcome_channel=guild.welcome_channel,
      welcome_message=guild.welcome_message
    ).WHERE(qb.EQUALS('id', guild.id)).get_query())

    self.update_welcome_image(guild.id, guild.welcome_image.to_blob())

  def update_welcome_image(self, id_: int, image: bytes):
    self.update(qb.UPDATE('welcome_image').SET(image=image).WHERE(qb.EQUALS('id', id_)).get_query())

  def update_event(self, event: mizu.classes.Event):
    self.update(qb.UPDATE('event').SET(state=event.state, datetime=event.datetime).WHERE(qb.EQUALS('guild_id', event.guild_id), qb.AND, qb.EQUALS('code', event.code)).get_query())



# def create_guild(self, guild_id: int) -> mizu.classes.Guild:
#     datetime_now = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
#     self.insert('INSERT INTO event VALUES(?, ?, ?, ?, ?);', (guild_id, 'DBA', 'Disboard Alert', datetime_now, 0))
#     self.insert('INSERT INTO event VALUES(?, ?, ?, ?, ?);', (guild_id, 'TPS', 'Template Sync', datetime_now, 0))


# def fetch_bank(self): # arrumar
#     return self.fetch(qb.SELECT(qb.ALL).FROM('bank').get_query())

#   def fetch_broker(self):
#     data = [list(x) for x in self.fetch(qb.SELECT(qb.ALL).FROM('broker').get_query())]
#     columns = self.fetch(qb.SELECT('name').FROM(qb.PRAGMA_TABLE_INFO('broker')).get_query())

#     stocks = {}
#     for stock in data:
#       items = {}
#       for column_name, item in zip(columns[1:], stock[1:]):
#         items[column_name[0]] = item

#       stocks[stock[0]] = items
#       stocks[stock[0]]['base_price'] = float(stocks[stock[0]]['base_price'])
#       stocks[stock[0]]['total_supply'] = int(stocks[stock[0]]['total_supply'])
#       stocks[stock[0]]['available_suply'] = int(stocks[stock[0]]['available_suply'])
#       stocks[stock[0]]['percent_change'] = float(stocks[stock[0]]['percent_change'])
#       try:
#         stocks[stock[0]]['history'] = Stack([float(x) for x in stocks[stock[0]]['history'].split('&')], use_deque=True, max_size=30, discard=True)

#       except ValueError:
#         stocks[stock[0]]['history'] = Stack(use_deque=True, max_size=30, discard=True)

#     return stocks

#   def fetch_broker_wallet(self):
    # users = self.fetch(qb.SELECT('user_id').FROM('broker_wallet').get_query())
    # data = [list(x) for x in self.fetch(qb.SELECT(qb.ALL).FROM('broker_wallet').ORDER_BY('user_id').get_query())]
    # columns = self.fetch(qb.SELECT('name').FROM(qb.PRAGMA_TABLE_INFO('broker_wallet')).get_query())

    # accounts = {}
    # for account in data:
    #   try:
    #     accounts[account[0]]

    #   except KeyError:
    #     accounts[account[0]] = {}

    #   idx = 0
    #   current_stock = ''

    #   for column_name, stock in zip(columns[1:], account[1:]):
    #     if idx == 0:
    #       accounts[account[0]][stock] = {}
    #       current_stock = stock

    #     else:
    #       accounts[account[0]][current_stock][column_name[0]] = stock

    #     idx += 1

    #   accounts[account[0]][current_stock]['quantity'] = int(accounts[account[0]][current_stock]['quantity'])
    #   accounts[account[0]][current_stock]['balance'] = float(accounts[account[0]][current_stock]['balance'])

    #   try:
    #     accounts[account[0]][current_stock]['history'] = Stack([float(x) for x in accounts[account[0]][current_stock]['history'].split('&')], use_deque=True)

    #   except ValueError:
    #     accounts[account[0]][current_stock]['history'] = Stack(use_deque=True)

    # return accounts