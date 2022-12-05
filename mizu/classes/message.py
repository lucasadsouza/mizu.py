from __future__ import annotations

import mizu.utils, mizu.classes
from mizu.classes import Base


class Message(Base):
  def __init__(self, db: mizu.utils.Koori, code: str):
    self.db = db
    self.code = code
    self.message = {}

  def add_message(self, language_code: str, message: str):
    self.message[language_code] = message

  def get_message(self, language: mizu.classes.Language, replaceable: list[any]=[]):
    if replaceable:
      return self.message[language.code].format(*replaceable)

    return self.message[language.code]


class ErrorMessage(Message):
  def __init__(self, db: mizu.utils.Koori, code: str):
    super().__init__(db, code)


class LogMessage(Message):
  def __init__(self, db: mizu.utils.Koori, code: str):
    super().__init__(db, code)
