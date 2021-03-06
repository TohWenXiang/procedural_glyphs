#!/usr/bin/env python3

import operator
from math import ceil
from random import randint
from functools import reduce


class Glyphs():

    BLOCK_BITS = 6


    def __init__(self, context, x_size, y_size, scale=10):

        self.context = context
        self.x_size  = x_size
        self.y_size  = y_size
        self.scale   = scale
        self.glyphs  = []


    def genGlyph(self):

        while True:
            length = self.getGlyphLength()
            glyph = randint(0, 2**length - 1) & randint(0, 2**length - 1)

            if glyph not in self.glyphs:
                print('created new glyph {:0{:d}x}'.format(glyph, int(ceil(length / 4))))
                return glyph

            print('collision on glyph {:0{:d}x}'.format(glyph, int(ceil(length / 4))))


    def drawLine(self, a, b, x_offset, y_offset):

        self.context.move_to(x_offset + a[0] * self.scale, y_offset + a[1] * self.scale)
        self.context.line_to(x_offset + b[0] * self.scale, y_offset + b[1] * self.scale)


    def drawBlock(self, block, x_offset, y_offset, leftEdge=False, topEdge=False, mirror=False):

        x = -1 if mirror else 1

        if topEdge: 
            if block & 1:
                self.drawLine((0, 0), (x, 0), x_offset, y_offset)
            block >>= 1

        if leftEdge:
            if block & 1:
                self.drawLine((0, 0), (0, 1), x_offset, y_offset)
            block >>= 1

        if block & 1:
            self.drawLine((0, 1), (x, 1), x_offset, y_offset)
        if block & 2:
            self.drawLine((x, 0), (x, 1), x_offset, y_offset)
        if block & 4:
            self.drawLine((0, 0), (x, 1), x_offset, y_offset)
        if block & 8:
            self.drawLine((0, 1), (x, 0), x_offset, y_offset)


    def drawGlyph(self, x_offset, y_offset, glyph=None):

        if glyph is None:
            glyph = self.genGlyph()

        for y in range(self.y_size):
            for x in range(self.x_size // 2):

                print('')
                print('x =', x)
                print('y =', y)
                print('getStartBit =', self.getStartBit(x, y))
                print('getBitWidth =', self.getBitWidth(x, y))


                block = glyph >> self.getStartBit(x, y) & (2**self.getBitWidth(x, y) - 1)

                self.drawBlock(block, x_offset + x * self.scale, y_offset + y * self.scale, 
                    leftEdge=(x == 0), topEdge=(y == 0))
                self.drawBlock(block, x_offset - x * self.scale, y_offset + y * self.scale, 
                    leftEdge=(x == 0), topEdge=(y == 0), mirror=True)


    def getBitWidth(self, x, y):

        return self.BLOCK_BITS - 2 + (x == 0) + (y == 0)


    def getStartBit(self, x, y):

        bit = 0
        for yy in range(self.y_size):
            for xx in range(self.x_size // 2):
                if xx == x and yy == y:
                    return bit
                bit += self.getBitWidth(xx, yy)


    def getGlyphLength(self):

        return ((self.BLOCK_BITS - 2) * self.x_size // 2 * self.y_size 
                + self.x_size // 2 + self.y_size)