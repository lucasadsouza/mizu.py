import sqlite3 as sqlite
from datetime import datetime, timezone

class KooriDB ():
  def __init__(self):
    self.connection = sqlite.connect('project/KooriDB.db')


  # Fetch all lines
  def fetch(self, query):
    cursor = self.connection.cursor()

    cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()

    return result


  # Fetch one line
  def fetchone(self, query):
    cursor = self.connection.cursor()

    cursor.execute(query)

    result = cursor.fetchone()
    cursor.close()

    return result


  def updateone(self, query):
    cursor = self.connection.cursor()

    cursor.execute(query)

    self.connection.commit()

    cursor.close()


  # Returns guild background welcome image
  def get_image(self, guild_id):
    image = self.fetchone(f'SELECT image FROM image WHERE guild_id = {guild_id};')

    path = 'project/src/images/background.jpg'
    with open(path, 'wb') as file:
      file.write(image[0])

    return path


  # Rerturns guild information
  def get_guild(self, guild_id, fields=None):
    if fields:
      guild = self.fetchone(f'SELECT {", ".join(fields)} FROM guild WHERE guild_id = {guild_id};')

      if len(fields) == 1:
        return guild[0]

      return guild

    else:
      guild = self.fetchone(f'SELECT language, log_channel, sync_channel, disboard_channel, welcome_channel, welcome_picture FROM guild WHERE guild_id = {guild_id};')

      return guild


  # Returns a constant
  def get_constant(self, const):
    constant = self.fetchone(f'SELECT constant FROM constant WHERE name = "{const}";')

    return constant[0]


  # Returns mizu messages
  def get_message(self, msg_code, lang):
    message = self.fetchone(f'SELECT message FROM mizu_message WHERE message_code = "{msg_code}" AND language = {lang}')

    return message[0]


  def get_event(self, event_code):
    event = self.fetchone(f'SELECT name, datetime, state FROM event WHERE code = "{event_code}"')

    event = (event[0], datetime.strptime(event[1], "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc), False if event[2] == 0 else True)

    return event

  def change_event_state(self, event_code):
    event = self.fetchone(f'SELECT state FROM event WHERE code = "{event_code}"')[0]

    if event == 0:
      self.updateone(f'UPDATE event SET state = {1} WHERE code = "{event_code}"')

    else:
      self.updateone(f'UPDATE event SET state = {0} WHERE code = "{event_code}"')

  def set_event_datetime(self, event_code, date_time):
    date_time = date_time.strftime("%Y-%m-%d %H:%M:%S.%f")

    self.updateone(f'UPDATE event SET datetime = "{date_time}" WHERE code = "{event_code}"')

  def get_color(self, format, color_name):
    return self.fetchone(f'SELECT {format} FROM color WHERE name = "{color_name}"')[0]
