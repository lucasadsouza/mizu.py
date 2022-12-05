import mizu.classes


def event_factory(params:list[any]=[]) -> mizu.classes.Event:
  event = mizu.classes.Event(*params)

  return event
