from __future__ import annotations

import mizu.utils
from mizu.classes import Base


class Language(Base):
  def __init__(self, db: mizu.utils.Koori, code: str, available: bool):
    self.db = db
    self.code = code
    self.available = available
    self.labels = {}

  def add_label(self, code:str, label:str):
    self.labels[code] = label
