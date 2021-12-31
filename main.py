from pygame.display import set_mode, set_caption, flip, get_surface
from pygame.event import get
from pygame.time import Clock
from pygame.draw import rect as drawrect
from pygame.font import SysFont
from pygame.image import load as imageload
from pygame.transform import scale

from pygame import QUIT, MOUSEBUTTONDOWN, init
from os import chdir
from json import load

init()
chdir('assets')
font = SysFont('Roboto', 64)


class Rect:
	def __init__(self, **kwargs):
		ws, hs = get_surface().get_size()
		self.origin = kwargs.get('origin') or (1, 1)
		rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
		x, y, w, h = rect
		self.rect = (int(ws*(x-w/2+w/2*self.origin[0])), int(hs*(y-w/2+h/2*self.origin[1])), int(ws*w), int(hs*h))
		self.color = kwargs.get('color') or (0, 0, 0)
		self.onclick = kwargs.get('onclick')
		self.loop = kwargs.get('loop')
		self.tags = []
	
	def setrect(self, **kwargs):
		ws, hs = get_surface().get_size()
		self.origin = kwargs.get('origin') or self.origin
		rect = kwargs.get('rect')
		if rect:
			x, y, w, h = rect
			self.rect = (int(ws*(x-w/2+w/2*self.origin[0])), int(hs*(y-w/2+h/2*self.origin[1])), int(ws*w), int(hs*h))
		self.color = kwargs.get('color') or self.color
		self.onclick = kwargs.get('onclick')
		self.loop = kwargs.get('loop')

	def getpos(self):
		ws, hs = get_surface().get_size()
		x, y, w, h = self.rect
		rect = (x/ws, y/hs, w/ws, h/hs)
		return rect


class Text:
	def __init__(self, **kwargs):
		global font
		self.text = kwargs.get('text') or 'None'
		self.color = kwargs.get('color') or (0, 0, 0)
		ws, hs = get_surface().get_size()
		self.origin = kwargs.get('origin') or (1, 1)
		rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
		x, y, w, h = rect
		self.rect = (int(ws*(x-w/2+w/2*self.origin[0])), int(hs*(y-w/2+h/2*self.origin[1])), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		self.onclick = kwargs.get('onclick')
		self.loop = kwargs.get('loop')
		self.tags = []
		
		self.surface = scale(font.render(self.text, True, self.color), self.size)
		
	def settext(self, **kwargs):
		global font
		self.text = kwargs.get('text') or self.text
		self.color = kwargs.get('color') or self.color
		ws, hs = get_surface().get_size()
		self.origin = kwargs.get('origin') or self.origin
		rect = kwargs.get('rect')
		if rect:
			x, y, w, h = rect
			self.rect = (int(ws*(x-w/2+w/2*self.origin[0])), int(hs*(y-w/2+h/2*self.origin[1])), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		self.onclick = kwargs.get('onclick')
		self.loop = kwargs.get('loop')
		
		self.surface = scale(font.render(self.text, True, self.color), self.size)

	def getpos(self):
		ws, hs = get_surface().get_size()
		x, y, w, h = self.rect
		rect = (x/ws, y/hs, w/ws, h/hs)
		return rect


class Image:
	def __init__(self, **kwargs):
		self.image = kwargs.get('image')
		rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
		ws, hs = get_surface().get_size()
		self.origin = kwargs.get('origin') or (1, 1)
		x, y, w, h = rect
		self.rect = (int(ws*(x-w/2+w/2*self.origin[0])), int(hs*(y-w/2+h/2*self.origin[1])), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		self.onclick = kwargs.get('onclick')
		self.loop = kwargs.get('loop')
		self.tags = []
		
		self.surface = scale(imageload(self.image), self.size)
		
	def setimage(self, **kwargs):
		self.image = kwargs.get('image') or self.image
		ws, hs = get_surface().get_size()
		self.origin = kwargs.get('origin') or self.origin
		rect = kwargs.get('rect')
		if rect:
			x, y, w, h = rect
			self.rect = (int(ws*(x-w/2+w/2*origin[0])), int(hs*(y-w/2+h/2*origin[1])), int(ws*w), int(hs*h))
		self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
		self.onclick = kwargs.get('onclick')
		self.loop = kwargs.get('loop')
		
		self.surface = scale(imageload(self.image), self.size)

	def getpos(self):
		ws, hs = get_surface().get_size()
		x, y, w, h = self.rect
		rect = (x/ws, y/hs, w/ws, h/hs)
		return rect


class Main:
	def __init__(self, **kwargs):
		self.width = kwargs.get('width') or 1280
		self.height = kwargs.get('height') or 720
		self.fps = kwargs.get('fps') or 60
		self.title = kwargs.get('title') or "Python Night Funkin"
		self.loop = True
		self.rects = []
		self.loops = []
		self.texts = []
		self.images = []
		self.onclicks = []
		
		self.screen = set_mode((self.width, self.height))
		set_caption(self.title)
		
	def event(self):
		for e in get():
			if e.type == QUIT:
				self.loop = False
			if e.type == MOUSEBUTTONDOWN:
				if e.button == 1:
					for i in self.onclicks:
						x, y, w, h = i.rect
						if x <= e.pos[0] <= x+w and y <= e.pos[1] <= y+h:
							i.onclick(i)
				
	def mainloop(self):
		cl = Clock()
		while self.loop:
			self.screen.fill((255, 255, 255))
			self.event()
			for i in self.loops:
				i.loop(i)
			self.render()
			flip()
			cl.tick(0)
			
	def render(self):
		for i in self.rects:
			drawrect(self.screen, i.color, i.rect)
		for i in self.images:
			self.screen.blit(i.surface, i.pos)
		for i in self.texts:
			self.screen.blit(i.surface, i.pos)
			
	def rect(self, **kwargs):
		obj = Rect(**kwargs)
		if kwargs.get('onclick'):
			self.onclicks += [obj]
		if kwargs.get('loop'):
			self.loops += [obj]
		self.rects += [obj]
		return obj
		
	def text(self, **kwargs):
		obj = Text(**kwargs)
		if kwargs.get('onclick'):
			self.onclicks += [obj]
		if kwargs.get('loop'):
			self.loops += [obj]
		self.texts += [obj]
		return obj
		
	def image(self, **kwargs):
		obj = Image(**kwargs)
		if kwargs.get('onclick'):
			self.onclicks += [obj]
		if kwargs.get('loop'):
			self.loops += [obj]
		self.images += [obj]
		return obj


with open('data/settings.json', 'r') as f:
	sets = load(f)


def play(obj):
	obj.tags = ['anim']


def playloop(obj):
	if 'anim' in obj.tags:
		x, y = obj.pos
		if obj.getpos()[1] > 0.5:
			print(obj.getpos())


main = Main(width=sets['width'], height=sets['height'], fps=sets['fps'], title=sets['title'])

playbtn = main.text(origin=(1, -1), rect=(0.1, 0.9, 0.1, 0.1), text='Play', onclick=play, loop=playloop)

main.mainloop()
