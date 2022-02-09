from nextcord.ext import commands, tasks
import nextcord

from datetime import datetime, timedelta

from modules import KooriDB, Welcome, CheckDisboard, AlertResetWeek, Event
from modules import Weather, Dictionary, Clean, Template, CheckPermissions
from modules import Settings, GetInfo




intents = nextcord.Intents.all()
game_activity = nextcord.Game(name='Development Tests. Version 1.5.0 - Beta', type=nextcord.ActivityType.playing)

bot = commands.Bot(command_prefix="!M", case_insensitive=False, activity=game_activity, intents=intents)




koori = KooriDB()
DISCORDTOKEN = koori.get_constant('DISCORDTOKEN')
WEATHERTOKEN = koori.get_constant('WEATHERTOKEN')


welcome = Welcome(bot, koori)
checkDisboard = CheckDisboard(bot, koori)
event = Event(bot, koori)
checkpermissions = CheckPermissions(koori)
settings = Settings(bot, koori, checkpermissions)
alertResetWeek = AlertResetWeek(bot, koori, event)
weather = Weather(WEATHERTOKEN, bot, koori)
dictionary = Dictionary(koori)
clean = Clean(koori)
template = Template(bot, koori, checkpermissions)
getinfo = GetInfo(koori)


event.run_events(['DMC', 'DBA', 'DRW'])

"""
EVENTS
"""

# Check if bot is connected and ready to work.
@bot.event
async def on_ready ():
  print(f'\nBOT NAME: {bot.user.name}')
  print(f'ID: {bot.user.id}')
  print(f'STATUS: online\n\n')


# Run on every message sent where the bot is listening.
@bot.event
async def on_message (message):
  # Logs users messages
  print(f'{message.guild.name} - #{message.channel.name}>> @{message.author.display_name}: {message.content}')

  for attachment in message.attachments:
    print(f'{attachment.filename} - {attachment.url}')

  for embed in message.embeds:
    print(f'{embed.title} - {embed.type}\n{embed.description}\n{embed.fields}\n{embed.footer}')

  # Check if the server was bumped successfully and register an alert to bump again
  await checkDisboard.bumped(message)

  # Allow commands be executed
  await bot.process_commands(message)


# Welcome a new member with a picture
@bot.event
async def on_member_join(member):
  await welcome.on_member_join(member)

# Send a message on server showind that someone left
async def on_member_remove(member):
  await welcome.on_member_remove(member)




"""
TASKS LOOP
"""

#An always loop that runs multiple actions.
@tasks.loop(seconds=10)
async def check_events():
  # if koori.get_event('DMC')[2]:
  #   print('Event now')
  #   koori.change_event_state('DMC')
  #   print(32 * '=')
  #   event.run_event('DMC', days=1)

  if koori.get_event('DRW')[2]:
    koori.change_event_state('DRW')
    await alertResetWeek.alert()


# Send a message before the check_events starts.
@check_events.before_loop
async def before_check_events ():
  await bot.wait_until_ready()

# Starts check_events.
check_events.start()




"""
COMMANDS
"""

# Alert to reset the week on Discloud
@bot.command(name='resetweek', aliases=['rw'])
async def alertDiscloudResetWeek(ctx):
  await alertResetWeek.reseted(ctx)


# Gets the current Weather by city
@bot.command(name='weather', aliases=['wtr'])
async def get_weather_by_city(ctx, city):
  await weather.get_weather(ctx, city)


# Gets dictionary definitions
@bot.group(invoke_without_command=True, name='dictionary', aliases=['dict'])
async def get_dictionary(ctx):
  await ctx.send('Try to use `!Mdictionary english` or `!Mdictionary japanese` instead')

# Gets dictionary definitions in English
@get_dictionary.command(name='english', aliases=['en'])
async def english_dictionary(ctx, word):
  await dictionary.english(ctx, word)

# Gets dictionary definitions in Japanese
@get_dictionary.command(name="japanese", aliases=['jp'])
async def japanese_dictionary(ctx):
  pass


# Delete a range of messages
@bot.group(invoke_without_command=True, name='clean')
async def clean_messages(ctx, range):
  await clean.clean(ctx, range)

# Delete a range of messages filtering by an user
@clean_messages.command(name='from')
async def clean_messages_from(ctx, from_, range):
  pass

# Delete a range of messages filtering by content
@clean_messages.command(name='contains')
async def clean_messages_containing(ctx, contains_, range):
  pass


# Handle guild's template
@bot.group(invoke_without_command=True, name='template', aliases=['tpt', 'gtp'])
async def guild_template(ctx):
  pass

# Create a guild template
@guild_template.command(name='new', aliases=['create', 'add'])
async def new_template(ctx, name, *, description=None):
  await template.new(ctx, name, description)

# Show a guild template
@guild_template.command(name='show', aliasses=['info'])
async def show_template(ctx):
  await template.show(ctx)

# Syncronize a guild template
@guild_template.command(name='syncronize', aliases=['sync', 'update'])
async def sync_template(ctx):
  await template.sync(ctx)

# Edit a guild template
@guild_template.command(name='edit')
async def edit_template(ctx):
  await template.edit(ctx)

# Delete a guild template
@guild_template.command(name='delete', aliases=['del'])
async def delete_template(ctx):
  await template.delete(ctx)


# Groups settings commands
@bot.group(invoke_without_command=True, name='settings', aliases=['set', 'configurations', 'configs'])
async def bot_settings(ctx):
  pass

# Groups Reset Week settings commands
@bot_settings.group(invoke_without_command=True, name='resetweek', aliases=['rw'])
async def settings_resetweek(ctx):
  pass

# Change the Reset Week channel id
@settings_resetweek.command(name='channel')
async def settings_resetweek_channel(ctx, channel_id):
  await settings.resetweek_channel(ctx, channel_id)

# Change the Reset Week role id
@settings_resetweek.command(name='role')
async def settings_resetweek_role(ctx, role_id):
  await settings.resetweek_role(ctx, role_id)

# Change the Reset Week language
@settings_resetweek.command(name='language', aliases=['lang'])
async def settings_resetweek_language(ctx):
  await settings.resetweek_language(ctx)


# Change the Daily Mizucoins time
@bot_settings.command(name='dailymizucoins', aliases=['dmc'])
async def settings_dailymizucoins_time(ctx, time):
  await settings.daily_mizucoins(ctx, time)


# Groups Guild settings commands
@bot_settings.group(invoke_without_command=True, name='guild', aliases=['server'])
async def settings_guild(ctx):
  pass

# Change the Guild id
@settings_guild.command(name='guild_id', aliases=['id', 'guild-id'])
async def settings_guild_id(ctx, guild_id, new_id):
  await settings.guild_id(ctx, guild_id, new_id)

# Change the Guild language
@settings_guild.command(name='language', aliases=['lang'])
async def settings_guild_language(ctx):
  await settings.guild_language(ctx)

# Change the Guild log channel id
@settings_guild.command(name='log_channel', aliases=['log-channel'])
async def settings_guild_log_channel(ctx, channel_id):
  await settings.guild_log_channel(ctx, channel_id)

# Change the Guild sync channel id
@settings_guild.command(name='sync_channel', aliases=['sync-channel'])
async def settings_guild_sync_channel(ctx, channel_id):
  await settings.guild_sync_channel(ctx, channel_id)

# Change the Guild Disboard channel id
@settings_guild.command(name='disboard_channel', aliases=['disboard-channel'])
async def settings_guild_disboard_channel(ctx, channel_id):
  await settings.guild_disboard_channel(ctx, channel_id)

# Change the Guild Disboard role id 
@settings_guild.command(name='disboard_role', aliases=['disboard-role'])
async def settings_guild_disboard_role(ctx, role_id):
  await settings.guild_disboard_role(ctx, role_id)

@settings_guild.command(name='welcome_channel', aliases=['welcome-channel'])
async def settings_guild_welcome_channel(ctx, channel_id):
  await settings.guild_welcome_channel(ctx, channel_id)

# Change the Guild welcome background
@settings_guild.command(name='welcome_background', aliases=['welcome_bg', 'welcome-background', 'welcome-bg'])
async def settings_guild_welcome_background(ctx):
  await settings.guild_welcome_background(ctx) # Not Working

# Change the Guild welcome message
@settings_guild.command(name='welcome_message', aliases=['welcome_msg', 'welcome-message', 'welcome-msg'])
async def settings_guild_welcome_message(ctx, *, message):
  await settings.guild_welcome_message(ctx, message)


# Get info about the guild and its members
@bot.group(invoke_without_command=True, name='get-info', aliases=['get'])
async def get_info(ctx):
  pass

@get_info.command(name='profile-picture', aliases=['pfp'])
async def get_info_profile_picture(ctx, member: nextcord.Member):
  await getinfo.profile_picture(ctx, member)

@get_info.command(name='emoji')
async def get_info_emoji(ctx, emoji: nextcord.Emoji):
  await getinfo.emoji(ctx, emoji)

@get_info_emoji.error
async def get_info_emoji_error(ctx, error):
  await ctx.send(error)


# Command to test commands
@bot.command(name='test')
async def test_func(ctx):
  # await alertResetWeek.reseted(ctx)
  # await settings.resetweek_language(ctx)
  # guild = bot.get_guild()
  # member = guild.get_member()
  # await welcome.on_member_join(member)
  pass



# Run the bot.
bot.run(DISCORDTOKEN)
