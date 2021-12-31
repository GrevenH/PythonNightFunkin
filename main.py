from pygame.display import set_mode, set_caption, flip, get_surface
from pygame.event import get
from pygame.time import Clock
from pygame.draw import rect as drawrect
from pygame.font import SysFont
from pygame.image import load as imageload
from pygame.transform import scale

from pygame import QUIT, MOUSEBUTTONDOWN, init
from os import chdir
from json import dump, load

init()
chdir('assets')
font = SysFont('Roboto', 48)


class Rect:
	def __init__(self, **kwargs):
		ws, hs = get_surface().get_size()
		rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
		x, y, w, h = rect
		self.rect = (int(ws*x), int(hs*y), int(ws*w), int(hs*h))
		self.color = kwargs.get('color') or (0, 0, 0)
	
	def setrect(self, **kwargs):
		ws, hs = get_surface().get_size()
		rect = kwargs.get('rect')
		if rect:
			x, y, w, h = rect
			self.rect = (int(ws*x), int(hs*y), int(ws*w), int(hs*h))
		self.color = kwargs.get('color') or self.color


class Text:
	def __init__(self, **kwargs):
		global font
		self.text = kwargs.get('text') or 'None'
		self.color = kwargs.get('color') or (0, 0, 0)
		ws, hs = get_surface().get_size()
		rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
		x, y, w, h = rect
		self.rect = (int(ws*x), int(hs*y), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		
		self.surface = scale(font.render(self.text, True, self.color), self.size)
		
	def settext(self, **kwargs):
		global font
		self.text = kwargs.get('text') or self.text
		self.color = kwargs.get('color') or self.color
		ws, hs = get_surface().get_size()
		rect = kwargs.get('rect')
		if rect:
			x, y, w, h = rect
			self.rect = (int(ws*x), int(hs*y), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		
		self.surface = scale(font.render(self.text, True, self.color), self.size)


class Image:
	def __init__(self, **kwargs):
		self.image = kwargs.get('image')
		rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
		ws, hs = get_surface().get_size()
		x, y, w, h = rect
		self.rect = (int(ws*x), int(hs*y), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		
		self.surface = scale(imageload(self.image), self.size)
		
	def setimage(self, **kwargs):
		self.image = kwargs.get('image') or self.image
		ws, hs = get_surface().get_size()
		rect = kwargs.get('rect')
		if rect:
			x, y, w, h = rect
			self.rect = (int(ws*x), int(hs*y), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		
		self.surface = scale(imageload(self.image), self.size)


class Main:
	def __init__(self, **kwargs):
		self.width = kwargs.get('width') or 1280
		self.height = kwargs.get('height') or 720
		self.fps = kwargs.get('fps') or 60
		self.title = kwargs.get('title') or "Python Night Funkin"
		self.loop = True
		self.rects = []
		self.texts = []
		self.images = []
		
		self.screen = set_mode((self.width, self.height))
		set_caption(self.title)
		
	def event(self):
		for e in get():
			if e.type == QUIT:
				self.loop = False
				
	def mainloop(self):
		while self.loop:
			self.screen.fill((255, 255, 255))
			self.event()
			self.render()
			flip()
			Clock().tick(self.fps)
			
	def render(self):
		for i in self.rects:
			drawrect(self.screen, i.color, i.rect)
		for i in self.images:
			self.screen.blit(i.surface, i.pos)
		for i in self.texts:
			self.screen.blit(i.surface, i.pos)
			
	def rect(self, **kwargs):
		obj = Rect()
		for i in kwargs:
			obj.__setattr__(i, kwargs[i])
		self.rects += [obj]
		return obj
		
	def text(self, **kwargs):
		obj = Text()
		for i in kwargs:
			obj.__setattr__(i, kwargs[i])
		self.texts += [obj]
		return obj
		
	def image(self, **kwargs):
		obj = Image()
		for i in kwargs:
			obj.__setattr__(i, kwargs[i])
		self.images += [obj]
		return obj


with open('data/settings.json', 'r') as f:
	sets = load(f)

main = Main(width=sets['width'], height=sets['height'], fps=sets['fps'], title=sets['title'])

main.rect(color=(255, 255, 0))
r = main.rect(rect=(0.2, 0.2, 0.1, 0.1))
print(r.rect)

main.mainloop()
