import collections
from collections.abc import Iterable
import mizu.classes


class Stack(mizu.classes.Base):
    def __init__(self, iterable: Iterable[any]=[], use_deque: bool=False, max_size: int=None, discard=False):
      self.use_deque = use_deque
      self.max_size = max_size
      self.discard = discard

      if use_deque:
        self._stack = collections.deque(iterable, maxlen=self.max_size)

      else:
        self._stack = list(iterable)

    def __repr__(self): # Returns the self._stack to print it
      return f'{list(self._stack)}'

    def __iter__(self): # Turns the Stack iterable
      for i in self._stack:
        yield i

    def is_empty(self):
      return True if len(self._stack) == 0 else False

    def is_full(self):
      return True if len(self._stack) == self.max_size else False

    def size(self):
      return len(self._stack)

    def top(self):
      return self._stack[-1]

    def push(self, item):
      if not self.discard and self.max_size != 0 and self.size() == self.max_size:
        raise Exception('Stack max size exceded.')

      self._stack.append(item)

    def pop(self):
      return self._stack.pop()

    def cut(self):
      self._stack.pop()

    def clear(self):
      self._stack.clear()

    def search(self, key: str, value: str):
      for item in self._stack:
        if item[key] == value:
          return item

      raise IndexError()
