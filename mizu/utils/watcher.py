from __future__ import annotations

import traceback, functools
import colorama
from nextcord.ext import commands
import mizu.classes, mizu.utils


class Watcher(mizu.classes.Base):
  def __init__(self, bot:commands.Bot, db: mizu.utils.Koori, log_channel:int, language: mizu.classes.Language):
    self.bot = bot
    self.db = db
    self.log_channel = log_channel
    self.language = language

  # Send bot logs to a specific guild channel
  async def log(self, log_code: str, replaceable: list[any]=[], class_: object=None, func: callable=None, send: bool=True):
    origin = []
    if class_:
      if class_.__class__.__module__:
          origin.append(class_.__class__.__module__)
      
      if class_.__class__.__qualname__:
        origin.append(class_.__class__.__qualname__)

      else:
        origin.append(class_.__class__.__name__)

    if func:
      origin.append(func.__name__)

    origin = '.'.join(origin)

    log_channel = self.bot.get_channel(self.log_channel)
    message = self.db.fetch_log_message(log_code).get_message(self.language, replaceable)

    if send:
      await log_channel.send(f'```json\n"{origin}:" {message}\n```')

    print(f'{colorama.Fore.BLUE}{origin}:{colorama.Fore.RESET} {message}')

  async def error(self, error: Exception, tb: traceback=None, send: bool=True):
    log_channel = self.bot.get_channel(self.log_channel)

    message = traceback.format_exception_only(type(error), error)[0]

    traceback_message = traceback.format_tb(tb)
    traceback_message[-1] = '{0}\n    {1}'.format(traceback_message[-1].split("\n")[0], message)
    traceback_message = '\n'.join(traceback_message)

    if send:
      await log_channel.send(f'```diff\n-{message}\n```\n```bash\n{traceback_message}\n```')

    print(f'{colorama.Fore.RED}{message}{colorama.Fore.RESET}\n\n{traceback_message}')
