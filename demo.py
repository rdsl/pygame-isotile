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
from engine import  *



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
        text_develop (pygame.sprite.RenderUpdates): Group for text sprites.
        develop (bool): Show technical info and windows.

    """

    def __init__(self):
        """Initialize and run the game."""
        pygame.display.set_caption('Pygame IsoTile Demo')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1024, 768))
        self.screen.fill((0, 0, 0))
        self.background = self.screen.copy()
        self.view_window = ViewWindow(200, 200, 800, 500)
        self.view = View(0, 0, *self.view_window.size)
        self.tile_set = TileSet()
        self.tile_map = TileMap()
        self.painter = Painter(self.view, self.view_window, self.tile_set,
                               self.tile_map)
        self.text_develop = pygame.sprite.RenderUpdates()
        self.develop = True
        self.draw_gui() #Called just once for now.
        self.run()


    def load_tile_map(self):
        """Load the tile map."""
        self.tile_map = TileMap()


    def load_tile_set(self):
        """Load the tile set."""
        self.tile_set = TileSet()


    def draw_gui(self):
        """Draw game GUI. Currently only draws the view window."""
        pygame.draw.rect(self.screen, (255, 255, 255),
                         self.view_window.inflate(2, 2), 1)
        pygame.display.flip()
    

    def update(self):
        """Perform game loop updates."""
        self.view.changed = False


    def event_handler(self, event):
        """Handle events."""
        view_dv = 10
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.view.move(dy = - view_dv)
            if event.key == K_DOWN:
                self.view.move(dy = view_dv)
            if event.key == K_LEFT:
                self.view.move(dx = - view_dv)
            if event.key == K_RIGHT:
                self.view.move(dx = view_dv)


    def run(self):
        """Game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                else:
                    self.event_handler(event)

            dirty_rects = []
            dirty_rects += self.painter.paint()
            self.screen.set_clip(None)

            if self.develop:  #Should get its own funcion or class.
                self.text_develop.clear(self.screen, self.background)
                #Render text for technical info.
                self.text_develop.empty()
                xc, yc = pygame.mouse.get_pos()
                xv, yv = (xc + self.view.rect.left  - self.view_window.left,
                          yc + self.view.rect.top - self.view_window.top)
                fps = self.clock.get_fps()
                fc = (200, 200, 200)
                texts = ['FPS: %.2f' % fps,
                         'VIEW: %i , %i' % self.view.rect.topleft,
                         'CUR (screen): %i, %i' % (xc, yc),
                         'CUR (view): %i, %i' % (xv, yv),
                         'CUR (map): %i, %i' % iso2top((xv, yv),
                                                       (self.tile_set.width,
                                                        self.tile_set.height))]
                for n, text in enumerate(texts):
                    TextSprite(text, 16, fc, (10, 10 * (n + 1), 0, 0)
                               ).add(self.text_develop)
                dirty_rects += self.text_develop.draw(self.screen)
                #Draw a zoom window. Class?
                clip = pygame.Surface((11, 11))
                clip.blit(self.screen, (0, 0), (xc - 5,  yc - 5, 11, 11))
                scaled = pygame.transform.scale(clip, (110, 110))
                rect = pygame.Rect(self.view_window.topright, (110, 110))
                rect.move_ip(-110, 0)
                scaled.fill((255, 0, 0), (50, 50, 10, 10))
                pygame.draw.rect(scaled, (255, 255, 255), scaled.get_rect(), 1)
                dirty_rects += [self.screen.blit(scaled,
                                                 (self.screen.get_width() -
                                                  120, 10))]

            pygame.display.update(dirty_rects)
            self.update()
            self.clock.tick(120)
                        



def main():
    """Initialize pygame and run the game."""
    pygame.init()
    pygame.key.set_repeat(100, 50)
    game = IT_Demo()



if __name__ == '__main__':
    main()
