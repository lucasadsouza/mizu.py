from __future__ import annotations

import nextcord
import mizu.classes, mizu.utils


class User(mizu.classes.Base):
  def __init__(self, observer: mizu.utils.Hermes, user_id: int, discord_user: nextcord.User, language: mizu.classes.Language, wallet: float, balance: float, is_dev: bool):
    self.observer = observer
    self.id = user_id
    self.raw = discord_user
    self.language = language
    self.wallet = wallet
    self.balance = balance
    self.is_dev = is_dev
