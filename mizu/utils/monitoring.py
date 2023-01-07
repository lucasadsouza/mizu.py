import os, asyncio
import psutil
from nextcord.ext import commands
from tqdm import tqdm

class Monitor():
  def __init__(self, bot: commands.Bot, update_rate: int=1):
    self.keep_measuring = True
    self.max_memory_usage = 0

    self.bot = bot
    self.update_rate = update_rate

  def get_max_memory(self) -> int:
    max_memory = 0

    max_memory = psutil.virtual_memory().total

    return max_memory

  def get_memory_usage(self) -> int:
    usage = 0

    process = psutil.Process(os.getpid())

    memory_info = process.memory_info()

    current_memory_usage = memory_info.vms
    self.max_memory_usage = max(current_memory_usage, self.max_memory_usage)

    return current_memory_usage

  def get_max_memory_usage(self) -> int:
    self.get_memory_usage()

    return self.max_memory_usage

  def generate_bar(self, total: int or float, current: int or float, label: str='', unit: str='', max_cols: int=20) -> str:
    if total > max_cols:
      bar_cols = max_cols
      bar_p_cols = round(current / (total / bar_cols))

    else:
      bar_cols = round(total)
      bar_p_cols = round(current)

    bar_n_cols = bar_cols - bar_p_cols

    return f'{label}: |{"█"*bar_p_cols}{" "*bar_n_cols}| {current}{unit}/{total}{unit}'

  async def monitor(self, max_memory: int=None):
    memorybar_total = round(max_memory / 1000000, 2)

    while self.keep_measuring:
      memory_usage = round(self.get_memory_usage() / 1000000, 2)
      progress_bar = f'{self.generate_bar(memorybar_total, memory_usage, "Memory usage", "Mb")}'

      print(progress_bar, end='\r')
      await asyncio.sleep(self.update_rate)

  async def discord_monitor(self, channel_id: int, max_memory: int=None):
    memorybar_total = round(max_memory / 1000000, 2)
    memory_usage = round(self.get_memory_usage() / 1000000, 2)
    progress_bar = f'```{self.generate_bar(memorybar_total, memory_usage, "Memory usage", "Mb")}```'
    
    channel = await self.bot.fetch_channel(channel_id)
    message = await channel.send(progress_bar)

    while self.keep_measuring:
      memory_usage = round(self.get_memory_usage() / 1000000, 2)
      progress_bar = f'```{self.generate_bar(memorybar_total, memory_usage, "Memory usage", "Mb")}```'

      await message.edit(progress_bar)
      await asyncio.sleep(self.update_rate)
