import nextcord

from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO


class Welcome():
  def __init__(self, bot, db):
    self.bot = bot
    self.db = db


  # Gets the background image.
  def get_background(self, guild_id, resolution):
    background_path = self.db.get_image(guild_id)

    background = Image.open(background_path)
    background = ImageOps.fit(background, resolution, method=3, bleed=0.0, centering=(0.5, 0.5)) # Refit the background.

    return background


  # Gets the dominant color of a picture.
  def get_dominant_color(self, img):
    img = img.copy()
    img.convert("RGB")
    img.resize((1, 1), resample=0)

    return img.getpixel((0, 0))


  # Gets the profile picture image.
  async def get_profile_picture(self, member, size, resolution):
    profile_picture = member.display_avatar.with_size(size)
    profile_picture = BytesIO(await profile_picture.read())
    profile_picture = Image.open(profile_picture)

    profile_picture.resize(resolution)

    return profile_picture


  # Transforms an image into a circle.
  def round_image(self, img):
    img = img.copy()
    bigsize_img = (img.size[0] * 3, img.size[1] * 3)

    mask = Image.new('L', bigsize_img, 0)

    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize_img, fill=255)
    
    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)

    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return img.resize((img.size[0]-30, img.size[1]-30), Image.ANTIALIAS)


  # Put the title and the shadow of the title on the image.
  def put_title(self, guild_id, member_name, img, title_y, dominant_color, main_color, font):
    img = img.copy()
    title = self.db.get_message('WLC001', self.db.get_guild(guild_id, ['language']))
    member_name = member_name + '!'

    titleW, titleH = font.getsize(title)
    member_nameW, member_nameH = font.getsize(member_name)

    img_draw = ImageDraw.Draw(img)

    img_draw.text(((img.size[0] - titleW) / 2, title_y), title, dominant_color, font=font) # Title shadow.
    img_draw.text(((img.size[0] - titleW) / 2, title_y - 3), title, (main_color), font=font) # Title

    img_draw.text(((img.size[0] - member_nameW) / 2, title_y + titleH), member_name, dominant_color, font=font) # Member name shadow
    img_draw.text(((img.size[0] - member_nameW) / 2, title_y + titleH - 3), member_name, (main_color), font=font) # Member name

    return img


  # Welcomes with a picture when a new member joins
  async def on_member_join(self, member):
    guild_id = member.guild.id

    background = self.get_background(guild_id, (416, 180))
    dominant_color = self.get_dominant_color(background)

    profile_picture = await self.get_profile_picture(member, 128, (120, 120))
    profile_picture = self.round_image(profile_picture)

    welcome_image = background.copy()
    welcome_image.paste(profile_picture, (int((background.size[0]/2) - (profile_picture.size[0]/2)), 10), profile_picture)

    font = ImageFont.truetype('project/src/fonts/UnDotumBold.ttf', 30)

    welcome_image = self.put_title(guild_id, member.display_name, welcome_image, 110, dominant_color, (255, 255, 255), font)
    welcome_image.save('project/src/images/welcome_picture.png')

    welcome_channel = self.db.get_guild(guild_id, ['welcome_channel'])
    welcome_channel = self.bot.get_channel(welcome_channel)

    await welcome_channel.send(f'<@!{member.id}>', file=nextcord.File('project/src/images/welcome_picture.png'))


  # Send a message on server showind that someone left
  async def on_member_remove(self, member):
    guild_id = member.guild.id
    welcome_channel = self.db.get_guild(member.guild.id, ['welcome_channel'])
    welcome_channel = self.bot.get_channel(welcome_channel)
    message = self.db.get_message('WLC002', self.db.get_guild(guild_id, ['language']))

    await welcome_channel.send(message.format(member.display_name))
