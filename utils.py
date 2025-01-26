# ******************************************************************************
# Copyright (c) 2024. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0 
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
# 
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
from dataclasses import dataclass

# ******************************************************************************
@dataclass
class BBox:
    x1: float = float('inf')
    y1: float = float('inf')
    x2: float = float('-inf')
    y2: float = float('-inf')

    def update(self, x1, y1, x2, y2):
        self.x1 = min(self.x1, x1)
        self.y1 = min(self.y1, y1)
        self.x2 = max(self.x2, x2)
        self.y2 = max(self.y2, y2)
        return self

    def addMargin(self, margin):
        self.x1 -= margin
        self.y1 -= margin
        self.x2 += margin
        self.y2 += margin
        return self

    @property
    def width(self):
        return self.x2 - self.x1

    @property    
    def height(self):
        return self.y2 - self.y1

    def __str__(self):
        return f'{self.x1:.2f} {self.y1:.2f} {self.x2:.2f} {self.y2:.2f}'

# ******************************************************************************
@dataclass
class GlyphInfo:
    gid: int
    x: int
    y: int
    xAdvance: int
    yAdvance: int
    cluster: int

    def update(self, txt: str) -> 'GlyphInfo':
        v = [int(x) for x in txt.split()]
        if len(v) != 6:
            raise ValueError(f'Invalid glyph info: {txt}')
        self.gid, self.x, self.y, self.xAdvance, self.yAdvance, self.cluster = v
        return self

    def __str__(self):
        return f'{self.gid} ({self.x},{self.y}) +{self.xAdvance}:{self.yAdvance} [{self.cluster}]'

# ******************************************************************************
