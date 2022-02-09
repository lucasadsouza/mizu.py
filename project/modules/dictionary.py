import requests, json

from nextcord import Embed


# Gets dictionaries definitions
class Dictionary():
  def __init__(self, db):
    self.db = db


  # Gets definitions in English
  async def english(self, ctx, word):
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{word.lower()}')

    # Handles if the word isn't found
    if response.status_code !=200:
      await ctx.send(self.db.get_message('DTC001', self.db.get_guild(ctx.guild.id, ['language'])))
      return False


    response = json.loads(response.content.decode('utf-8'))[0]

    word_definition = {'title': f"**{response['word'].upper()}** - {response['phonetics'][0]['text']}\n", 'content': []}

    for i in range(0, len(response['meanings'])):
      word_definition['content'].append([
        f"**{response['meanings'][i]['partOfSpeech'].capitalize()}**",
        f"{response['meanings'][i]['definitions'][0]['definition']}\n\n*- {response['meanings'][i]['definitions'][0]['example'].capitalize()}.*\n‏‏‎ ‎"
      ])


    embed = Embed(title = word_definition['title'], description = '‏‏‎ ‎', colour = 14423100)

    for i in range(0, len(word_definition['content'])):
      embed.add_field(name=word_definition['content'][i][0], value=word_definition['content'][i][1], inline=False)

    await ctx.send(embed=embed)
