import mizu.classes


def language_factory(params:list[any]=[], labels:list[tuple[str]]=[]) -> mizu.classes.Language:
  language = mizu.classes.Language(*params)

  for label in labels:
    language.add_label(*label)

  return language
