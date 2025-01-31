# ******************************************************************************
# Copyright (c) 2024. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
#
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
from dataclasses import dataclass
from collections import namedtuple
from pathlib import Path
from typing import List
import re

# CATEGORIES *******************************************************************
CATEGORIES = ('Cc|Cf|Cs|Co|Cn|'
              'Ll|Lu|Lt|Lm|Lo|'
              'Mn|Mc|Me|'
              'Nd|Nl|No|'
              'Pc|Pd|Ps|Pe|Pf|Pi|Po|'
              'Sm|Sc|Sk|So|'
              'Zs|Zl|Zp').split('|')
CATEGORIES.sort()


# BLOCKS ***********************************************************************
Block = namedtuple('Block', ['start', 'end', 'name'])
BLOCKS: List[Block] = []
BLOCK_FILEPATH: Path = Path('Blocks.txt')
assert(BLOCK_FILEPATH.exists())

reComment: str = r'^\s*#.*$'
# """Match a complete line of text that start with optional whitespace characters,
# followed by the hash symbol `#`, and then any number of
# non-whitespace characters till the end of the line"""
reBlockRange: str = r'^\s*([0-9A-Fa-f]+)\.\.([0-9A-Fa-f]+)\s*;\s*(.*)\s*$'
# """Match three groups, two hexadecimal codes separated by two dots `..` followed
# by a a semicolon `;` and additional text till end of the line"""

# Read the UNICODE standard blocks text file and extract the ranges and the
# respective block names. Assumes `Blocks.txt` file.
bftxt = BLOCK_FILEPATH.read_text(encoding='utf8')
lines = [l for l in bftxt.splitlines() if l.strip()]

for line in lines:
    if re.search(reComment, line):
        continue

    match = re.search(reBlockRange, line)
    if match:
        BLOCKS.append(Block(start=int(match.group(1), 16),
                            end=int(match.group(2), 16),
                            name=match.group(3)))

# Helper function to find the block of given character unicode
def findBlock(n: int) -> int:
    """Find the index of the block that contains the given unicode value.

    Parameters:
        n(int): The unicode value to find.

    Returns:
        The index of the block that contains the given unicode value,
        or -1 if it is not found.
    """
    left, right = 0, len(BLOCKS) - 1

    while left <= right:
        mid = (left + right) // 2

        # Check if n is within the current range
        if BLOCKS[mid].start <= n <= BLOCKS[mid].end:
            return mid  # Return the index of the range that contains n

        # Decide which half to search next
        if n < BLOCKS[mid].start:
            right = mid - 1
        else:
            left = mid + 1

    return -1  # Return -1 if n does not fall within a    for b in BLOCKS:

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
