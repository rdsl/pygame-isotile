# IsoTile: A tile based isometric game engine.
# Copyright (C): 2016, Ramiro Duarte Simoes Lopes
#
# This file is part of IsoTile
#
# IsoTile is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""IsoTile: A pygame isometric tile engine.

(In development).
Provides a minimum set of classes for a tile based isometric game.

"""


import os
import pygame
from pygame.locals import *



class TextSprite(pygame.sprite.Sprite):

    """A simple text sprite.

    Attributes:

        text (str): Rendered text.
        size (int): Font size.
        color (tuple): Font color.
        rect (pygame.Rect): Image rectangle.
        fontfile (str): Font pathname.
        bg (tuple): Background color.
        aa (bool): Antialias.

    """

    def __init__(self, text, size, color, rect, fontfile=None, bg=None,
                 aa=False):
        """Initialize instance.

        Call self.render to set sprite image.

        Args:
            text (str): Text to be rendered.
            size (int): Font size.
            color (tuple): Font color.
            rect (pygame.Rect): Rect-like object. Size is ignored.
            fontfile (str, optional): Font pathname.
            bg (tuple, optional): Background color.
            aa (bool, optional): Antialias.

        """
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.size = size
        self.color = color
        self.rect = pygame.Rect(rect) 
        self.fontfile = fontfile
        self.bg = bg
        self.aa = aa
        self.render()

    def render(self):
        """Render text image and set rect size."""
        font = pygame.font.Font(self.fontfile, self.size)
        if self.bg:
            self.image = font.render(self.text, self.aa, self.color, self.bg)
        else:
            self.image = font.render(self.text, self.aa, self.color)
        self.rect.size = self.image.get_rect().size



def load_image(name, colorkey=(255, 255, 255)):
    """Load image, convert and return surface."""
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    image.set_colorkey(colorkey)
    return image


def iso2top((x, y), (tw, th)):
    """Receive screen coordinates and return map coordinates.""" 
    x, y, tw, th = [float(n) for n in (x, y, tw, th)]
    return int(y / th - x / (tw + 2.)) , int(y / th + x / (tw + 2.))


def top2iso((i, j), (tw, th)):
    """Receive map coordinates and return screen coordinates.""" 
    return j * (tw / 2 + 1) - i * (tw / 2 + 1) , (i + j) * th / 2



class TileSet(object):

    """Provide a TileSet object.

    Currently, a skeleton class.

    Attributes:
        width (int): Tile width.
        height (int): Tile height.
        level (int): Map level height.
        tiles (dic): Holds tiles, keys are tile numbers.

    """

    def __init__(self):
        """Initialize the class."""
        self.temp_sheet()

    def temp_sheet(self):
        """Initialize demo tile set."""
        self.width = 130
        self.height = 66
        self.level = 66
        self.tiles = dict()
        for i in range(2):
            self.tiles[i] = {'type': 'floor',
                             'image': load_image('%i.png' %i),
                             'offset': (- self.width / 2, 0)}
        for i in range(2, 4):
            self.tiles[i] = {'type': 'wall',
                             'image': load_image('%i.png' %i),
                             'offset': (-66, -66)}
        self.tiles[3]['offset'] = (0, -66)



class TileMap(object):

    """Provide a TileMap object.

    Currently a skeleton class.

    Attributes:
        map (dic): Holds the world map. Keys are (i, j) coordinates and values
                   are a list of lists of tiles.
        ni (int): Number of rows.
        nj (int): Number of columns.

    """

    def __init__(self):
        """Initialize the class."""
        self.temp_map()

    def temp_map(self):
        """Initialize demo tile map."""
        self.map = dict()
        self.ni = 20
        self.nj = 20
        for i in range(self.ni):
            for j in range(self.nj):
                walls = []
                self.map[(i, j)] = [[1], walls, []]
        self.map[(9,9)][1] = [2]
        self.map[(10,9)][1] = [2]
        self.map[(7,7)][1] = [3]
        self.map[(7,8)][1] = [3]
        self.map[(11,11)][1] = [2,3]
        self.map[(11,9)][1] = [2]
        self.map[(10,12)][1] = [2]
        self.map[(12,9)][1] = [3]
        self.map[(12,10)][1] = [3]



class View(object):

    """A camera view in world pixel coordinates.

    Coordinate origin is center (tile width / 2) of tile (0, 0)

    Attributes:
        rect (pygame.Rect): Position and size.
        changed (bool): Change state.

    """

    def __init__(self, x, y, w, h):
        """Initializes the view.

        Args:
            x (int): x position in pixel coordinates.
            y (int): y position in pixel coordinates.
            w (int): view width - should be equal to the view window's width.
            h (int): view height - should be equal to the view window's height.

        """
        self.rect = pygame.Rect(x, y, w, h)
        self.changed = True

    def move(self, x=0, y=0, dx=0, dy=0):
        """Move the view and set self.changed True.

        Should be called with either x and y or dx and dy.

        Args:
            x (int, optional): new x position in pixel coordinates.
            y (int, optional): new y position in pixel coordinates.
            dx (int, optional): x displacement in pixel coordinates.
            dy (int, optional): y displacement in pixel coordinates.

        """
        if dx != 0 or dy != 0:
            self.rect.move_ip(dx, dy)
        else:
            self.rect.topleft = (x, y)
        self.changed = True



ViewWindow = pygame.Rect  #ViewWindow class, just an alias for rect for now.



class Painter(object):

    """The Painter.

    Paints isometric tiles to the view window. In its current state it could be
    just a function, but future functionalities await.

    Attributes:
        screen (pygame.Surface): Pygame display surface.
        view (View): Camera view.
        view_window (ViewWindow): Screen view window.
        tile_set (TileSet): Tile set.
        tile_map (TileMap): Tile map.
        text_group (pygame.sprite.RenderUpdates): Group to hold text sprites
                   tied to the view. Cleared everytime the view changes.

    """

    def __init__(self, view, view_window, tile_set, tile_map):
        """Initialize Painter.

        Args:
            view (View): Camera view.
            view_window (ViewWindow): Screen view window.
            tile_set (TileSet): Tile set.
            tile_map (TileMap): Tile map.

        """
        self.screen = pygame.display.get_surface()
        self.view = view
        self.view_window = view_window
        self.tile_set = tile_set
        self.tile_map = tile_map
        self.text_group = pygame.sprite.RenderUpdates()

    def paint(self, show_grid=True, develop=True):
        """Paints isometric tiles to the screen.

        Find possibly visible tiles based on view geometry, loop over them,
        test if inside view then blit it to the screen. Draw sprites.
        Return list with dirty rectangles.

        Args:
            show_grid (bool): Paint grid.
            develop (bool): Paint develop info.

        """
        dirty_rects = []
        self.screen.set_clip(self.view_window)
        if self.view.changed:
            self.text_group.empty()
            self.screen.fill((10, 10, 10), self.view_window)
            dirty_rects += [self.view_window]
            itl, jtl = iso2top(self.view.rect.topleft,
                               (self.tile_set.width, self.tile_set.height))
            itr, jtr = iso2top(self.view.rect.topright,
                               (self.tile_set.width, self.tile_set.height))
            ibr, jbr = iso2top(self.view.rect.bottomright,
                               (self.tile_set.width, self.tile_set.height))
            ibl, jbl = iso2top(self.view.rect.bottomleft,
                               (self.tile_set.width, self.tile_set.height))
            i0 = min(max(0, itr), self.tile_map.ni) #min i
            i1 = min(max(0, ibl)+1, self.tile_map.ni) #max i
            j0 = min(max(0, jtl), self.tile_map.nj)
            j1 = min(max(0, jbr)+1, self.tile_map.nj)
            for i in range(i0, i1):
                for j in range(j0, j1):
                    xs, ys = top2iso((i, j), (self.tile_set.width,
                                              self.tile_set.height))
                    xs += self.view_window.left - self.view.rect.left
                    ys += self.view_window.top - self.view.rect.top
                    
                    for tilegroup in self.tile_map.map[(i, j)]:
                        for tileind in tilegroup:
                            tile = self.tile_set.tiles[tileind]
                            xt = xs + tile['offset'][0]
                            yt = ys + tile['offset'][1]
                            if (xt + self.tile_set.width > self.view_window.left and
                                xt < self.view_window.right and
                                yt + self.tile_set.height > self.view_window.top and
                                yt < self.view_window.bottom):
                                self.screen.blit(tile['image'], (xt, yt))
                    
                                if show_grid:
                                    grid = self.tile_set.tiles[0]
                                    gx = xs + grid['offset'][0]
                                    gy = ys + grid['offset'][1]
                                    self.screen.blit(grid['image'], (gx, gy))

                                if develop:
                                    tile_text = TextSprite('%i , %i' % (i, j),
                                          12, (200, 200, 200),
                                          (xs, ys + self.tile_set.height / 2.,
                                           0, 0))
                                    self.text_group.add(tile_text)
        dirty_rects += self.text_group.draw(self.screen)
        return dirty_rects
