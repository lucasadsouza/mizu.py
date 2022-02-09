from datetime import datetime, timedelta
import requests, json, os

from nextcord import Embed


# Gets current weather by city
class Weather():
  def __init__(self, token, bot, db):
    self.token = token
    self.bot = bot
    self.db = db
    self.colors = ('01d', '02d', '03d', '10d') # Icons with orange color


  # Fetch weather from OpenWeatherMap
  def fetch_weather(self, city):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.token}&units=metric')

    return json.loads(response.content) # Request content


  # Creates an embed.
  def generates_embed(self, weather, lang):
    color = self.db.get_color('decimal', 'Gray')
    if weather['weather'][0]['icon'] in self.colors:
      color = self.db.get_color('decimal', 'LightOrange')

    timezone = ((datetime.utcnow() + timedelta(seconds=weather['timezone'])).time()).strftime("%H:%M:%S") # Converts UTC to localtime
    week = datetime.today().strftime('%A') # Today weekday converted to fullname
    name = weather['name'] # City name
    flag = f':flag_{weather["sys"]["country"].lower()}:' # Flag emoji
    main_weather = weather['weather'][0]['main'] # Current weather type
    temp = weather['main']['temp'] # Current temperature in Celcius
    temp_min = weather['main']['temp_min'] # Minimum temperature in Celcius
    temp_max = weather['main']['temp_max'] # Maximum temperature in Celcius
    wind_speed = weather['wind']['speed'] # Wind speed in m/s
    humidity = weather['main']['humidity'] # Weather humidity in percentage
    icon = f"https://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png" # Current weather icon


    embed = Embed(title=f'{name} {flag} - {main_weather}', description=' ‎', colour=color)

    embed.add_field(
      name=self.db.get_message('WTR001', lang).format(week),
      value=self.db.get_message('WTR002', lang).format(temp, temp_min, temp_max, wind_speed, humidity).replace(r'\n', '\n'),
      inline=False
    )

    embed.add_field(name=self.db.get_message('WTR003', lang), value=f'{timezone}\n ‎', inline=False)

    embed.set_footer(text=self.db.get_message('WTR004', lang))
    embed.set_thumbnail(url=icon)

    return embed


  # Gets the current weather
  async def get_weather(self, ctx, city):
    guild_lang = self.db.get_guild(ctx.guild.id, ['language'])

    weather = self.fetch_weather(city.lower())
    embed = self.generates_embed(weather, guild_lang)

    await ctx.send(embed=embed)
