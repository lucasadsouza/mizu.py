from mizu.classes import Base


class Color(Base):
  def __init__(self, name: str, decimal: int=None, ANSI: str=None):
    self.name = name
    self.decimal = decimal
    self.ANSI = ANSI
