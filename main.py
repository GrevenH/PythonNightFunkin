#########################
#                       #
#  Python Night Funkin  #
#                       #
#########################


# Imports
from json import load, dump
from os import chdir

from pygame import QUIT, MOUSEBUTTONDOWN, init
from pygame.display import set_mode, set_caption, flip, get_surface
from pygame.draw import rect as drawrect
from pygame.event import get
from pygame.font import SysFont
from pygame.image import load as imageload
from pygame.time import Clock
from pygame.transform import scale

init()  # Init pygame
chdir('Assets')  # Change path to Assets
font = SysFont('Arial Black', 64)  # Init font

WHITE = (255, 255, 255)  # Init white color
BLACK = (0, 0, 0)  # Init black color


class Object:
    def __init__(self):
        self.rect = None
        self.pos = None

    def setpos(self, **kwargs):
        ws, hs = get_surface().get_size()
        pos = kwargs.get('pos')
        (x, y), (w, h) = pos, (ws / self.rect[2], hs / self.rect[3])
        self.pos = (int(ws * x), int(hs * y))
        x, y = self.pos
        self.rect = (x, y, w, h)

    def getrect(self):
        ws, hs = get_surface().get_size()
        x, y, w, h = self.rect
        rect = (x / ws, y / hs, w / ws, h / hs)
        return rect

    def getpos(self):
        ws, hs = get_surface().get_size()
        x, y, w, h = self.rect
        pos = (x / ws, y / hs)
        return pos


class Rect(Object):  # Class for rect objects
    def __init__(self, **kwargs):
        ws, hs = get_surface().get_size()
        self.origin = kwargs.get('origin') or (1, 1)
        rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
        x, y, w, h = rect
        self.rect = (
            int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])), int(ws * w),
            int(hs * h))
        self.color = kwargs.get('color') or (0, 0, 0)
        self.onclick = kwargs.get('onclick')
        self.loop = kwargs.get('loop')

    def rerender(self, **kwargs):
        ws, hs = get_surface().get_size()
        self.origin = kwargs.get('origin') or self.origin
        rect = kwargs.get('rect')
        if rect:
            x, y, w, h = rect
            self.rect = (
                int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])),
                int(ws * w),
                int(hs * h))
        self.color = kwargs.get('color') or self.color
        self.onclick = kwargs.get('onclick') or self.onclick
        self.loop = kwargs.get('loop') or self.loop

    def setrect(self, **kwargs):
        ws, hs = get_surface().get_size()
        pos = kwargs.get('pos')
        x, y, w, h = self.rect
        x, y = pos
        self.origin = kwargs.get('origin') or self.origin
        self.rect = int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])), w, h

    def getpos(self):
        ws, hs = get_surface().get_size()
        x, y, w, h = self.rect
        pos = (x / ws, y / hs)
        return pos


class Text(Object):  # Class for text objects
    def __init__(self, **kwargs):
        global font
        self.text = kwargs.get('text') or 'None'
        self.color = kwargs.get('color') or (0, 0, 0)
        ws, hs = get_surface().get_size()
        self.origin = kwargs.get('origin') or (1, 1)
        rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
        x, y, w, h = rect
        self.rect = (
            int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])), int(ws * w),
            int(hs * h))
        self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
        self.onclick = kwargs.get('onclick')
        self.loop = kwargs.get('loop')

        self.surface = scale(font.render(self.text, True, self.color), self.size)

    def rerender(self, **kwargs):
        global font
        self.text = kwargs.get('text') or self.text
        self.color = kwargs.get('color') or self.color
        ws, hs = get_surface().get_size()
        self.origin = kwargs.get('origin') or self.origin
        rect = kwargs.get('rect')
        if rect:
            x, y, w, h = rect
            self.rect = (
                int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])),
                int(ws * w),
                int(hs * h))
        self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
        self.onclick = kwargs.get('onclick') or self.onclick
        self.loop = kwargs.get('loop') or self.loop

        self.surface = scale(font.render(self.text, True, self.color), self.size)


class Image(Object):  # Class for image objects
    def __init__(self, **kwargs):
        self.image = kwargs.get('image')
        rect = kwargs.get('rect') or (0.1, 0.1, 0.1, 0.1)
        ws, hs = get_surface().get_size()
        self.origin = kwargs.get('origin') or (1, 1)
        x, y, w, h = rect
        self.rect = (
            int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])), int(ws * w),
            int(hs * h))
        self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
        self.onclick = kwargs.get('onclick')
        self.loop = kwargs.get('loop')

        self.surface = scale(imageload(self.image), self.size)

    def rerender(self, **kwargs):
        self.image = kwargs.get('image') or self.image
        ws, hs = get_surface().get_size()
        self.origin = kwargs.get('origin') or self.origin
        rect = kwargs.get('rect')
        if rect:
            x, y, w, h = rect
            self.rect = (
                int(ws * (x - w / 2 + w / 2 * self.origin[0])), int(hs * (y - w / 2 + h / 2 * self.origin[1])),
                int(ws * w),
                int(hs * h))
        self.pos, self.size = (self.rect[0], self.rect[1]), (self.rect[2], self.rect[3])
        self.onclick = kwargs.get('onclick') or self.onclick
        self.loop = kwargs.get('loop') or self.loop

        self.surface = scale(imageload(self.image), self.size)


class Main:  # Main application class
    def __init__(self, **kwargs):
        self.width = kwargs.get('width') or 1280
        self.height = kwargs.get('height') or 720
        self.fps = kwargs.get('fps') or 60
        self.title = kwargs.get('title') or 'Python Night Funkin'
        self.loop = True
        self.objs = []
        self.rects = []
        self.texts = []
        self.images = []
        self.onclicks = []

        self.screen = set_mode((self.width, self.height))
        set_caption(self.title)

    def event(self):  # Event listener
        for e in get():
            if e.type == QUIT:
                self.loop = False
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    for i in self.onclicks:
                        x, y, w, h = i.rect
                        if x <= e.pos[0] <= x + w and y <= e.pos[1] <= y + h:
                            i.onclick(i)

    def mainloop(self):  # Main loop
        cl = Clock()
        while self.loop:
            self.screen.fill(WHITE)
            self.event()
            for i in self.objs:
                if i.loop:
                    i.loop(i)
            self.render()
            flip()
            cl.tick(self.fps)

    def render(self):  # Render objects
        for i in self.rects:
            drawrect(self.screen, i.color, i.rect)
        for i in self.images:
            self.screen.blit(i.surface, i.pos)
        for i in self.texts:
            self.screen.blit(i.surface, i.pos)

    def remove(self, obj):  # Remove object from lists
        if type(obj) == Rect:
            self.rects.pop(self.rects.index(obj))
        elif type(obj) == Text:
            self.texts.pop(self.texts.index(obj))
        elif type(obj) == Image:
            self.images.pop(self.images.index(obj))
        else:
            return False
        self.objs.pop(self.objs.index(obj))

    def rect(self, **kwargs):  # Draw rect
        obj = Rect(**kwargs)
        if kwargs.get('onclick'):
            self.onclicks += [obj]
        self.rects += [obj]
        self.objs += [obj]
        return obj

    def text(self, **kwargs):  # Draw text
        obj = Text(**kwargs)
        if kwargs.get('onclick'):
            self.onclicks += [obj]
        self.texts += [obj]
        self.objs += [obj]
        return obj

    def image(self, **kwargs):  # Draw image
        obj = Image(**kwargs)
        if kwargs.get('onclick'):
            self.onclicks += [obj]
        self.images += [obj]
        self.objs += [obj]
        return obj


with open('data/settings.json', 'r') as f:
    sets = load(f)  # Import settings

with open('data/levels.json', 'r') as f:
    lvls = load(f)

##############################
#                            #
#  Graphical User Interface  #
#                            #
#       ↓     ↓     ↓        #
#                            #
##############################


def playclick(obj):
    obj.loop = playloop


def playloop(obj):
    global levelbtns
    x, y = obj.getpos()
    obj.setpos(pos=(x - 0.005, y))

    if obj.getpos()[0] <= 0:
        obj.loop = None
        main.remove(obj)
        x, y = 0, 1

        for i in lvls:
            w, h = i['text_size']
            y -= 0.1
            lvl = main.text(text=i['text'], rect=(x, y, w, h), color=WHITE, origin=(1, -1), loop=levelloop,
                            onclick=levelclick)
            lvl.namespace = i['namespace']
            levelbtns += [lvl]


def levelclick(obj):
    global levelbtns

    for i in levelbtns:
        main.remove(i)
    with open(f'data/game/{obj.namespace}/players.json', 'r') as f:
        players = load(f)
    with open(f'data/game/{obj.namespace}/song.json', 'r') as f:
        song = load(f)
    
    x, y = players['second']['pos']
    w, h = players['second']['size']
    background.rerender(image=f'images/game/{obj.namespace}/background.png')
    second = main.image(image=f"images/game/{obj.namespace}/players/second/{players['second']['images']['passive'][0]}",
                        loop=secondloop, rect=(x, y, w, h))
    second.passiveimages = players['second']['images']['passive']

    imgs = []
    for i in second.passiveimages:
        imgs += [f"images/game/{obj.namespace}/players/second/{i}"]

    second.passiveimages = imgs
    second.song = song
    second.namespace = obj.namespace
    second.rpt = True


def levelloop(obj):
    x, y = obj.getpos()
    obj.setpos(pos=(x + 0.005, y))

    if obj.getpos()[0] >= 0.1:
        obj.loop = None


def firstloop(obj):
    pass


def secondloop(obj):
    if obj.rpt:
        if len(obj.passiveimages) > obj.passiveimages.index(obj.image)+1:
            obj.rerender(image=obj.passiveimages[obj.passiveimages.index(obj.image)+1])
        else:
            obj.rerender(image=obj.passiveimages[0])


levelbtns = []

main = Main(width=sets['width'], height=sets['height'], fps=sets['fps'], title=sets['title'])  # Creating window

# Objects
background = main.image(rect=(0, 0, 1, 1), image='images/menu/background.png')
playbtn = main.text(origin=(1, -1), rect=(0.1, 0.9, 0.12, 0.1), color=WHITE, text='Play', onclick=playclick)
vertxt = main.text(origin=(1, -1), rect=(0.02, 1, 0.05, 0.03), text=sets['version'], color=BLACK)

main.mainloop()  # Calling main loop
