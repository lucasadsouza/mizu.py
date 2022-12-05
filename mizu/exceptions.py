from __future__ import annotations

import mizu.classes, mizu.utils


class ErrorRaiser():
  def __init__(self, db: mizu.utils.Koori, language: mizu.classes.Language):
    self.db = db
    self.language = language
  
  def raise_error(self, type: str, error_code: str):
    if type == 'constant':
      raise ConstantError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'color':
      raise ColorError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'language':
      raise LanguageError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'message':
      raise MessageError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'user':
      raise UserError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'member':
      raise MemberError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'event':
      raise EventError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'guild':
      raise GuildError(self.db.fetch_error_message(error_code).get_message(self.language))

    elif type == 'image':
      raise ImageError(self.db.fetch_error_message(error_code).get_message(self.language))


class ConstantError(Exception):
  """Raise exceptions related to constants."""

class ColorError(Exception):
  """Raise exceptions related to the Color class."""

class LanguageError(Exception):
  """Raise exceptions related to the Language class."""

class MessageError(Exception):
  """Raise exceptions related to the Message class."""

class UserError(Exception):
  """Raise exceptions related to the User class."""

class MemberError(Exception):
  """Raise exceptions related to the Member class."""

class EventError(Exception):
  """Raise exceptions related to the Event class."""

class GuildError(Exception):
  """Raise exceptions related to the Guild class."""

class ImageError(Exception):
  """Raise exceptions related to the Image class."""
