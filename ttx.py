# ******************************************************************************
# Copyright (c) 2024. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0 
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
# 
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
from shiny import reactive
from shiny.express import module, ui, render

from fontTools import ttLib
from fontTools.pens.svgPathPen import SVGPathPen

from .utils import BBox

# ******************************************************************************
@module
def modTtx(input, output, session):
    # Data ---------------------------------------------------------------------
    @reactive.calc
    def ttFont():
        files = input.ttxFile()
        if files is None:
            return None
        
        if len(files) < 1:
            return None

        fileData: dict = files[0]
        if 'datapath' not in fileData:
            return None

        try:
            tt = ttLib.TTFont(fileData['datapath'])
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

        return tt
    
    @reactive.calc
    def maxBBox() -> BBox | None:
        tt = ttFont()
        if tt is None:
            return None
    
        bbMax = BBox()

        glyfTable = tt['glyf']
        for glyphName in tt.getGlyphOrder():
            metrics = glyfTable[glyphName]
            
            xMin = getattr(metrics, 'xMin', 0)
            yMin = getattr(metrics, 'yMin', 0)
            xMax = getattr(metrics, 'xMax', 0)
            yMax = getattr(metrics, 'yMax', 0)
            
            bbMax.update(x1=xMin, y1=yMin, x2=xMax, y2=yMax)
        
        bbMax.addMargin(100)

        return bbMax
    
    with ui.card(class_='bg-light border-dark'):
        ui.input_file("ttxFile", "Choose a font file:",
                      accept=['.ttf', '.otf', '*.*'],
                      multiple=False)

    @render.express
    def inputGlyphCount():
        tt = ttFont()
        if tt is not None:
            total = len(tt.getGlyphOrder())
            if total > 0:
                with ui.layout_columns(col_widths=(4, 2)):
                    ui.input_slider("glyphCount", "Number of Glyphs:",
                                    min=1, max=total,
                                    value=[0, 9] if total >= 10 else [0, total-1])
                    ui.input_action_button("updateTable", "Update")
                ui.tags.hr()

    @module
    def glyphImage(input, output, session, gid):
        @render.express
        def renderGlyph():
            tt = ttFont()
            if tt is None:
                return
            
            pen = SVGPathPen(None)
            glyphName = tt.getGlyphOrder()[gid]
            glyphSet = tt.getGlyphSet()
            pen = SVGPathPen(glyphSet)

            glyph = glyphSet[glyphName]
            glyph.draw(pen)

            bbMax = maxBBox()

            glyfTable = tt['glyf']
            metrics = glyfTable[glyphName]
            bbGlyph = BBox(
                x1 = getattr(metrics, 'xMin', 0),
                y1 = getattr(metrics, 'yMin', 0),
                x2 = getattr(metrics, 'xMax', 0),
                y2 = getattr(metrics, 'yMax', 0)
            )

            ui.tags.svg(
                ui.tags.Tag('rect',
                            x=bbGlyph.x1, y=bbGlyph.y1,
                            width=bbGlyph.width, height=bbGlyph.height,
                            style="fill:none;stroke:green;stroke-width:10"),

                # ui.tags.Tag('rect',
                #             x=bbMax.x1, y=bbMax.y1,
                #             width=bbMax.width, height=bbMax.height,
                #             style="fill:none;stroke:blue;stroke-width:5"),

                ui.tags.Tag('line',
                            x1=f'{bbMax.x1}', y1='0',
                            x2=f'{bbMax.x2}', y2='0',
                            stroke="red", stroke_width="5"),
                ui.tags.Tag('line',
                            x1=f'0', y1=f'{bbMax.y1}',
                            x2=f'0', y2=f'{bbMax.y2}',
                            stroke="red", stroke_width="5"),

                ui.tags.Tag('path',
                            d=pen.getCommands()),
                width=100,
                height=100,
                xmlns='http://www.w3.org/2000/svg',
                viewBox= f'{bbGlyph.x1-50:.2f} {bbMax.y1:.2f} {bbGlyph.width+100:.2f} {bbMax.height:.2f}',
                transform='matrix(1, 0, 0, -1, 0, 0)'
            )
    
    @reactive.event(input.updateTable)
    def countRange():
        return input.glyphCount()

    @render.express
    def renderGlyphTablle():
        tt = ttFont()
        if tt is not None:
            with ui.layout_column_wrap(width=1/6):
                vi, vf = countRange()
                for i in range(vi, vf):
                    glyphName = tt.getGlyphOrder()[i]
                    with ui.card(): 
                        ui.card_header(f'{glyphName} [{i}]')
                        glyphImage(f'gid{i}', gid=i)
