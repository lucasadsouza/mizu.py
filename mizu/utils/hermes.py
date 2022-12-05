import mizu.classes


class Hermes(mizu.classes.Base):
  _subscribers = {}
  _async_subscribers = {}

  def subscribe(self, type:str, fn:callable):
    if not type in self._subscribers:
      self._subscribers[type] = []

    self._subscribers[type].append(fn)

  def notify(self, type:str, data:list[any]):
    if type in self._subscribers:
      for fn in self._subscribers[type]:
        fn(*data)

  def async_subscribe(self, type:str, fn:callable):
    if not type in self._async_subscribers:
      self._async_subscribers[type] = []

    self._async_subscribers[type].append(fn)

  async def async_notify(self, type:str, data:list[any]):
    if type in self._async_subscribers:
      for fn in self._async_subscribers[type]:
        await fn(*data)
