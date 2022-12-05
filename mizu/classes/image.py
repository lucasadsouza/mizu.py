from __future__ import annotations

import os, copy, io
import nextcord
import PIL.Image, PIL.ImageOps, PIL.ImageDraw, PIL.ImageFont, PIL.ImageFilter
import mizu.utils
from mizu.classes import Base


class Image(Base):
  def __init__(self, image: bytes or tuple[int, int, str]=(600, 600, '#FFFFFF'), font: str='src/fonts/Murecho.ttf'):
    self.font = font
    self.has_mask = False
    self.elements = mizu.utils.Stack()

    if isinstance(image, bytes):
      self.image = PIL.Image.open(io.BytesIO(image))

    else:
      self.image = self.create_canvas(image[0], image[1], image[2])

    self.dominant_color = self.get_dominant_color()
    self.rendered_image = self.image

    self.add_element('img_0', None, None, self)

  def save(self, name: str, folder: tuple[str]):
    path = ''
    for f in folder:
      path = os.path.join(path, f)
      if not os.path.exists(path):
        os.mkdir(path)

    self.image.save(os.path.join(*folder, f'{name}.png'))

  def undo(self):
    self.elements.cut()

  def show(self):
    self.rendered_image.show()

  def to_bytes(self):
    img_bytes_arr = io.BytesIO()
    self.rendered_image.save(img_bytes_arr, format='PNG')
    img_bytes_arr.seek(0)

    return img_bytes_arr

  def clone(self) -> Image:
    return copy.deepcopy(self)

  def create_canvas(self, width: int, height: int, color: str):
    return PIL.Image.new('RGB', (width, height), color)

  def fit(self, width: tuple[int], height: tuple[int]):
    self.image = PIL.ImageOps.fit(
      self.image,
      (width, height),
      method=3, bleed=0.0, centering=(0.5, 0.5)
    )

    return self

  def get_dominant_color(self) -> tuple[int]:
    image = self.image.copy()
    image.convert('RGB')
    image = image.resize((1, 1), resample=0)

    return image.getpixel((0, 0))

  def is_light(self):
    image = self.image.copy()
    image.convert('RGB')
    image = image.resize((10, 10), resample=0)
    image_colors = image.getcolors()

    average_image_colors = []
    for image_color in image_colors:
      average_image_colors.append(sum(image_color[1]) / 3)

    average_color = sum(average_image_colors) / len(average_image_colors)

    return False if average_color < 127.5 else True

  def get_size(self, coordenate: str='xy') -> int or tuple[int]:
    if coordenate == 'x':
      return self.image.size[0]

    elif coordenate == 'y':
      return self.image.size[1]

    return self.image.size

  def resize(self, width: tuple[int], height: tuple[int]) -> Image:
    self.image = self.image.resize((width, height), PIL.Image.ANTIALIAS)

    return self

  def border_radius(self, radius: int=0, round: bool=False, border: int=0, border_color: str or tuple[int]=(0, 0, 0)) -> Image:
    if round:
      radius = self.image.size[0] * 2

    mask_ratio = (self.image.size[0] * 3, self.image.size[1] * 3)

    mask = PIL.Image.new('L', mask_ratio)
    draw = PIL.ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + mask_ratio, fill=255, radius=radius)

    mask = mask.resize(self.image.size, PIL.Image.ANTIALIAS)

    self.image.putalpha(mask)

    border_mask = PIL.Image.new('RGBA', mask_ratio)
    draw = PIL.ImageDraw.Draw(border_mask)
    draw.rounded_rectangle((0, 0) + mask_ratio, fill=0, outline=border_color, width=border, radius=radius)
    border_mask = border_mask.resize(self.image.size, PIL.Image.ANTIALIAS)

    self.image.alpha_composite(border_mask)

    self.has_mask = True

    return self

  def border(self, border_thickness: int=0, color: str='#000000'):
    if self.image.mode == "RGB":
      alpha_channel = PIL.Image.new('L', self.image.size, 255) # 'L' 8-bit pixels, black and white
      self.image.putalpha(alpha_channel)

    border_img = PIL.ImageOps.expand(self.image, border=border_thickness, fill=color)
    self.image = border_img

    return self

  def blur(self, radius: int) -> Image:
    self.image = self.image.filter(PIL.ImageFilter.GaussianBlur(radius))

    return self

  def has_transparency(self):
    if self.image.info.get("transparency", None) is not None:
        return True

    if self.image.mode == "P":
      transparent = self.image.info.get("transparency", -1)
      for _, index in self.image.getcolors():
        if index == transparent:
          return True

    elif self.image.mode == "RGBA":
      extrema = self.image.getextrema()
      if extrema[3][0] < 255:
        return True

    return False

  def paste_image(self, image: Image, position: tuple[int]=(0, 0), align_by_center: bool=False) -> Image:
    if align_by_center:
      position = (int(position[0] - (image.get_size('x') / 2)), int(position[1] - (image.get_size('y') / 2)))

    if image.has_mask or image.has_transparency():
      self.image.paste(image.image, position, image.image)

    else:
      self.image.paste(image.image, position)

    return self

  def write(self, text: str, font_size: int=12, color: str='#000000', position: tuple[int]=(0, 0), padding=False, align_by_center: bool=False, shadow: bool=False, shadow_color: str or tuple[int] or bool=False, adjust: bool=False) -> Image:
    font = PIL.ImageFont.truetype(self.font, font_size)

    textW, textH = font.getbbox(text)[2:]
    anchor = 'lt'

    if padding:
      position = [position[0] + padding[3], position[1] + padding[0]]

      if position[0] + textW + padding[1] > self.get_size('x') and not adjust:
        position[0] = position[0] - (position[0] + textW + padding[1] - self.get_size('x'))

      if position[0] < padding[3]:
        position[0] = padding[3]

      if position[1] + textH + padding[2] > self.get_size('y'):
        position[1] = position[1] - (position[1] + textH + padding[2] - self.get_size('y'))

      if position[1] < padding[0]:
        position[1] = padding[0]

    if adjust:
      text_max_length = self.get_size('x') - position[0] - (padding[1] if padding else 0)
      while(font.getlength(text) > text_max_length):
        font_size -= 1
        font = PIL.ImageFont.truetype(self.font, font_size)

      # if padding:
      #   position[1] += textH - font.getbbox(text)[2:][1]

    if align_by_center:
      anchor = 'mm'

    if not shadow_color:
      shadow_color = self.dominant_color

    if shadow:
      draw = PIL.ImageDraw.Draw(self.image)
      draw.text((position[0], position[1] + 3), text, shadow_color, font=font, anchor=anchor)

    draw = PIL.ImageDraw.Draw(self.image)
    draw.text(position, text, color, font=font, anchor=anchor)

    return self

  def add_element(self, img_id: str, fn: str=None, param: list[any]=None, image: Image=None):
    self.elements.push([img_id, fn, param, image.to_bytes().getvalue() if image else None])

  def render(self, replacebles: list[tuple[str]]=()):
    images = {}
    for element in self.elements:
      if isinstance(element[3], bytes):
        images[element[0]] = Image(element[3])
        continue

      if element[1] == 'paste_image':
        element[2][0] = images[element[2][0]]

      elif element[1] == 'write':
        for replaceble in replacebles:
          element[2][0] = element[2][0].replace(replaceble[0], replaceble[1])

      getattr(images[element[0]], element[1])(*element[2])

    self.rendered_image = images['img_0'].image

    return self


class ImageElement(Image):
  def __init__(self, image: PIL.Image, font: str=None):
    super().__init__(image, font)
    self.image = image


class WelcomeImage(Image):
  def __init__(self, image: bytes, font: str=None):
    super().__init__(image, font)
    self.recipe = mizu.utils.Stack()

  async def get_user_pfp(self, member: nextcord.Member, size: int):
    pfp = member.display_avatar.with_size(size)
    pfp = Image(await pfp.read(), 'src/fonts/Murecho.ttf')

    return pfp

  def add_ingredient(self, img_id: str=None, fn: str=None, param: list[any]=None, image: Image=None):
    self.recipe.push([img_id, fn, param, image.to_bytes().getvalue() if image else image])

  def undo_recipe(self):
    self.recipe.cut()


  def bake_recipe(self, member_name=''):
    images = {}
    for ingredient in self.recipe:
      if isinstance(ingredient[3], bytes):
        images[ingredient[0]] = Image(ingredient[3], 'src/fonts/Murecho.ttf')
        continue

      if ingredient[1] == 'put_image':
        ingredient[2][0] = images[ingredient[2][0]]

      if ingredient[1] == 'write':
        ingredient[2][0] = ingredient[2][0].replace('@member', member_name)

      getattr(images[ingredient[0]], ingredient[1])(*ingredient[2])

    return images['img_0']

  async def on_join(self, member: nextcord.Member):
    pfp = await self.get_user_pfp(member, 128)

    recipe = [
      ['img_0', None, None, pfp],
      ['img_0', 'fit', [180, 180], None],
      ['img_0', 'border_radius', [0, True, 20, 'white'], None],
      ['img_0', 'resize', [120, 120], None],

      ['img_1', None, None, self],
      ['img_1', 'fit', [416, 180], None],
      ['img_1', 'blur', [5], None],
      ['img_1', 'put_image', ['img_0', (85, 90), True], None],

      ['img_1', 'write', ['Bem-vindo(a),', 28, 'white', (155, 65), False, False, True, False, False], None],
      ['img_1', 'write', ['@member!', 28, 'white', (155, 95), (0, 15, 0, 0), False, True, False, True], None],

      ['img_1', 'show', [], None]
    ]

    for item in recipe:
      self.add_ingredient(*item)

    self.bake_recipe(member.display_name)
