import json
from typing import Union

class TextComponent(object):
	def __init__(
	 self,
	 color: str = "",
	 bold: bool = False,
	 italic: bool = False,
	 underlined: bool = False,
	 strikethrough: bool = False,
	 obfuscated: bool = False,
	 font: str | None = None
	):
		self.color = color
		self.bold = bold
		self.italic = italic
		self.underlined = underlined
		self.strikethrough = strikethrough
		self.obfuscated = obfuscated
		self.font = font
		self.extra: list[TextComponent] = []

	def format(self) -> dict:
		ret: dict = dict()
		if self.color: ret['color'] = self.color
		if self.bold: ret['bold'] = self.bold
		if self.italic: ret['italic'] = self.italic
		if self.underlined: ret['underlined'] = self.underlined
		if self.strikethrough: ret['strikethrough'] = self.strikethrough
		if self.obfuscated: ret['obfuscated'] = self.obfuscated
		if self.font: ret['font'] = self.font
		if self.extra: ret['extra'] = [i.dict() for i in self.extra]
		return ret

	def dict(self) -> dict:
		raise NotImplementedError('Empty component.')
	
	def json(self) -> str:
		return json.dumps(self.dict(), ensure_ascii=False)
	
	def __add__(self, other: Union['TextComponent', str]) -> 'TextComponent':
		if isinstance(other, TextComponent):
			self.extra.append(other)
			return self
		elif isinstance(other, str):
			self.extra.append(Literal(other))
			return self
		else: raise TypeError('Cannot add non-TextComponent object to TextComponent.')


class Literal(TextComponent):
	def __init__(self, text: str,
			  color: str = "",
			  bold: bool = False,
			  italic: bool = False,
			  underlined: bool = False,
			  strikethrough: bool = False,
			  obfuscated: bool = False,
			  font: str | None = None) -> None:
		super().__init__(color, bold, italic, underlined, strikethrough, obfuscated, font)
		self.text = text

	def dict(self):
		ret = self.format()
		ret['text'] = self.text
		return ret


class Translatable (TextComponent):
	def __init__(self, key: str, fallback: str | None = None, args: list[TextComponent] | None = None,
			  color: str = "",
			  bold: bool = False,
			  italic: bool = False,
			  underlined: bool = False,
			  strikethrough: bool = False,
			  obfuscated: bool = False,
			  font: str | None = None) -> None:
		super().__init__(color, bold, italic, underlined, strikethrough, obfuscated, font)
		self.key = key
		self.fallback=fallback
		self.args = args

	def dict(self):
		ret = self.format()
		ret['translate'] = self.key
		if self.fallback is not None:
			ret['fallback'] = self.fallback
		if self.args:
			ret['with'] = []
			for arg in self.args:
				ret['with'].append(arg.dict())
		return ret


class Score (TextComponent):
	def __init__(self, name: str, objective: str, value: str | None = None,
			  color: str = "",
			  bold: bool = False,
			  italic: bool = False,
			  underlined: bool = False,
			  strikethrough: bool = False,
			  obfuscated: bool = False,
			  font: str | None = None) -> None:
		super().__init__(color, bold, italic, underlined, strikethrough, obfuscated, font)
		self.name = name
		self.objective = objective
		self.value = value

	def dict(self):
		ret = self.format()
		ret['score'] = {'name':self.name,'objective':self.objective}
		if self.value:
			ret['score']['value'] = self.value
		return ret
	
class Selector (TextComponent):
	def __init__(self, selector: str, separator: TextComponent | None = None,
			  color: str = "",
			  bold: bool = False,
			  italic: bool = False,
			  underlined: bool = False,
			  strikethrough: bool = False,
			  obfuscated: bool = False,
			  font: str | None = None) -> None:
		super().__init__(color, bold, italic, underlined, strikethrough, obfuscated, font)
		self.selector = selector
		self.separator = separator

	def dict(self):
		ret = self.format()
		ret['selector'] = self.selector
		if self.separator:
			ret['separator'] = self.separator.dict()
		return ret

class Keybind (TextComponent):
	def __init__(self, keybind: str,
			  color: str = "",
			  bold: bool = False,
			  italic: bool = False,
			  underlined: bool = False,
			  strikethrough: bool = False,
			  obfuscated: bool = False,
			  font: str | None = None) -> None:
		super().__init__(color, bold, italic, underlined, strikethrough, obfuscated, font)
		self.keybind = keybind

	def dict(self):
		ret = self.format()
		ret['keybind'] = self.keybind
		return ret


class TextList (object):
	def __init__(self, context: list[TextComponent] = []):
		self.context = context
	
	def list(self) -> list:
		ret = list()
		for i in self.context:
			ret.append(i.dict())
		return ret
	
	def json(self) -> str:
		return json.dumps(self.list(), ensure_ascii=False)