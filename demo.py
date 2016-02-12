#! /usr/bin/python2
# -*- coding: utf-8 -*-

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


"""IsoTile Demo: A demo for IsoTile.

(In development).
A map explorer to test, develop and demonstrate IsoTile.

"""


import pygame
from pygame.locals import *
from engine import  TileMap, TileSet, View, ViewWindow, Painter



class IT_Demo(object):

    """Game class.

    Very simple map explorer.

    Attibutes:
        clock (pygame.time.Clock): A clock.
        screen (pygame.Surface): Display surface.
        view_window (engine.ViewWindow): Map view window.
        view (engine.View): Camera view.
        tile_set (engine.TileSet): Game tile set.
        tile_map (engine.TileMap): Game tile map.
        painter (engine.Painter): Painter.

    """

    def __init__(self):
        """Initialize and run the game."""
        pygame.display.set_caption('Pygame IsoTile Demo')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1024, 768))
        self.view_window = ViewWindow(200, 200, 800, 500)
        self.view = View(0, 0, *self.view_window.size)
        self.tile_set = TileSet()
        self.tile_map = TileMap()
        self.painter = Painter(self.view, self.view_window, self.tile_set,
                               self.tile_map)
        self.run()


    def load_tile_map(self):
        """Load the tile map."""
        self.tile_map = TileMap()


    def load_tile_set(self):
        """Load the tile set."""
        self.tile_set = TileSet()
    

    def update(self):
        """Perform game loop updates."""
        self.view.changed = False


    def event_handler(self, event):
        """Handle events."""
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.view.move(dy = -1)
            if event.key == K_DOWN:
                self.view.move(dy = 1)
            if event.key == K_LEFT:
                self.view.move(dx = -1)
            if event.key == K_RIGHT:
                self.view.move(dx = 1)


    def run(self):
        """Game loop."""
        while True:
            self.clock.tick(60)
            self.painter.paint()
            self.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                else:
                    self.event_handler(event)



def main():
    """Initialize pygame and run the game."""
    pygame.init()
    pygame.key.set_repeat(100, 50)
    game = IT_Demo()



if __name__ == '__main__':
    main()
