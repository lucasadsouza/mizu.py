import inspect


class Base():
  def get_class_name(self):
    if self.__class__.__qualname__:
      name = self.__class__.__qualname__

    elif self.__class__.__name__:
      name = self.__class__.__name__

    return name

  def get_class_fullname(self):
    name = self.get_class_name()

    if self.__class__.__module__:
      module = self.__class__.__module__.replace(f'.{name.lower()}', '')

      return f'{module}.{name}'
    
    return name

  def __repr__(self):
    attributes = inspect.getmembers(self, lambda x:not(inspect.isroutine(x)))
    attributes = [ x for x in attributes if not(x[0].startswith('__') and x[0].endswith('__')) ]
    
    att = []
    for x in attributes:
      x = list(x)
      if type(x[1]) == list:
        x[1] = 'list'

      if type(x[1]) == dict:
        x[1] = 'dict'

      if type(x[1]) == str:
        if len(x[1]) > 25:
          x[1] = x[1][:25] + '...'
      
      att.append(x)
  
    att = [ f'{x[0]}: {x[1]}' for x in att if not(x[0].startswith('__') and x[0].endswith('__')) ]

    return f'<{self.get_class_fullname()} {", ".join(att)}>'

  def update(self):
    print(self.get_class_name(), self)
