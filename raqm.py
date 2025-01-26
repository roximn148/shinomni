# ******************************************************************************
# Copyright (c) 2024. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0 
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
# 
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
from functools import reduce
import math
from pathlib import Path
import tempfile
from subprocess import run

import cairo
from shiny import reactive
from shiny.express import module, ui, render

from fontTools import ttLib
from fontTools.pens.svgPathPen import SVGPathPen

from .utils import BBox, GlyphInfo

# ******************************************************************************
RAQM = '/home/roximn/projects/libraqm/build/src/raqm'

# ******************************************************************************
@module
def modRaqm(input, output, session):
    # Font file ----------------------------------------------------------------
    @reactive.calc
    def ttFontFile():
        files = input.raqmFile()
        if files is None:
            return None
        
        if len(files) < 1:
            return None

        fileData: dict = files[0]
        if 'datapath' not in fileData:
            return None
        
        return fileData['datapath']

    @reactive.calc
    def ttFont():
        fontFile = ttFontFile()
        if fontFile is None:
            return None
        
        try:
            tt = ttLib.TTFont(fontFile)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

        return tt
    
    # Maximum bounding box -----------------------------------------------------
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
    
    # Font File Selection ------------------------------------------------------
    with ui.card(class_='bg-light border-dark'):
        with ui.layout_columns(col_widths=(8, 2, 2)):
            ui.input_file("raqmFile", "Choose a font file:",
                          accept=['.ttf', '.otf', '*.*'],
                          multiple=False)
            ui.input_radio_buttons("textDirection", "Direction:",
                                   {"rtl": "RTL", "ltr": "LTR"})
            ui.input_select("textLanguage", "Language:",
                            {"urd": "Urdu", "ara": "Arabic", "fas": "Persian",
                             "pus": "Pashto", "snd": "Sindhi", "eng": "English"})

    # Text Input ---------------------------------------------------------------
    with ui.card(class_='bg-light border-dark'):
        ui.input_text("textInput", "", placeholder="Enter text to render", width='100%')

    @module
    def textImage(input, output, session, gis: list[GlyphInfo]):
        @render.express
        def renderSvgText():
            tt = ttFont()
            if tt is None:
                return
            
            go = tt.getGlyphOrder()
            glyphNames = [go[gi.gid] for gi in gis]
            glyphSet = tt.getGlyphSet()

            paths = []
            x, y, dx = 0, 0, 50
            for gn, gi in zip(glyphNames, gis):
                glyph = glyphSet[gn]
                pen = SVGPathPen(glyphSet)

                glyph.draw(pen)
                commands = pen.getCommands()

                x += gi.x
                y += gi.y
                print(f"Rendering glyph {gi.gid} at ({x}, {y})")
                paths.append(
                    ui.tags.Tag('path',
                                d=commands,
                                transform=f'translate({x}, {y})',
                                fill='blue',
                                stroke='none')
                )
                paths.append(
                    ui.tags.Tag('line',
                                x1=f'{x-dx}', y1=f'{y}',
                                x2=f'{x+dx}', y2=f'{y}',
                                stroke="red", stroke_width="10")
                )
                paths.append(
                    ui.tags.Tag('line',
                                x1=f'{x}', y1=f'{y-dx}',
                                x2=f'{x}', y2=f'{y+dx}',
                                stroke="red", stroke_width="10")
                )

                x += gi.xAdvance
                y += gi.yAdvance

            bbMax = maxBBox()
            W = x
            
            ui.tags.svg(
                ui.tags.Tag('line',
                            x1=f'{0}', y1='0',
                            x2=f'{W}', y2='0',
                            stroke="red", stroke_width="5"),
                ui.tags.Tag('line',
                            x1=f'{0}', y1=f'{bbMax.y1:.2f}',
                            x2=f'{0}', y2=f'{bbMax.y2:.2f}',
                            stroke="red", stroke_width="5"),
                *paths,
                width=1200,
                height=400,
                xmlns='http://www.w3.org/2000/svg',
                viewBox= f'{bbMax.x1:.2f} {bbMax.y1:.2f} {W} {bbMax.height:.2f}',
                transform='matrix(1, 0, 0, -1, 0, 0)'
            )

    # Cairo Text Rendering -----------------------------------------------------
    @render.express
    def renderText():
        def showMessage(msg: str):
            ui.notification_show(msg, type='message', duration=2, id='renderNotification')

        def showError(msg: str):
            ui.notification_show(msg, type='error', duration=10, id='errorNotification')

        def drawGlyph(ctx: cairo.Context, gid, x, y, color, dx, dy, ax, ay, W, H, outline=False):
            ctx.save()
            ctx.translate(x, y)

            glRun = [cairo.Glyph(gid, dx, dy)]

            if outline:
                ctx.set_source_rgba(color[0], color[1], color[2], 0.25)
                ctx.arc(0, 0, 3, 0, 2 * math.pi)
                ctx.stroke_preserve()
                ctx.fill()

                extents = ctx.glyph_extents(glRun)
                # print(f'{extents.x_bearing},{extents.y_bearing} '
                #       f'{extents.width}:{extents.height} - '
                #       f'{extents.x_advance}:{extents.y_advance}')

                ctx.set_line_width(1)
                ctx.rectangle(extents.x_bearing, extents.y_bearing, extents.width, extents.height)
                ctx.stroke()
                ctx.set_line_width(2)
                ctx.rectangle(extents.x_bearing + dx, extents.y_bearing + dy, extents.width, extents.height)
                ctx.stroke()

                ctx.set_line_width(1)
                ctx.move_to(extents.x_bearing, extents.y_bearing)
                ctx.rel_line_to(dx, dy)
                ctx.stroke()

                if ax:
                    ctx.set_line_width(1)
                    ctx.move_to(ax, -H)
                    ctx.line_to(ax, +H)
                    ctx.stroke()

                if ay:
                    ctx.set_line_width(1)
                    ctx.move_to(-W, ay)
                    ctx.line_to(+W, ay)
                    ctx.stroke()

            ctx.set_source_rgba(*color, 1.0)
            ctx.show_glyphs(glRun)

            ctx.restore()


        ttf = ttFontFile()
        tt = ttFont()
        txt = input.textInput()
        if ttf is None or not txt:
            return
        
        fontName = tt['name'].getName(1, 3, 1).toUnicode()
        direction = input.textDirection()
        lang = input.textLanguage()

        defaultColor = (0, 1, 1)
        WIDTH, HEIGHT = 1200, 200
        SZ = 48
        MARGIN = 100
        EMF = SZ / tt['head'].unitsPerEm

        def getGlyphInfo(tt, txt: str, direction: str, lang: str):
            result = run([RAQM, tt, txt, direction, lang],
                            text=True, capture_output=True, check=True)
            output = result.stdout.splitlines()[1:]
            gi = [GlyphInfo(*[int(x) for x in line.split(' ')])for line in output]
            return gi

        if ttf is not None and txt:
            try:
                gInfos = getGlyphInfo(ttf, txt, direction, lang)
                showMessage(f"{len(gInfos)} glyphs rendered.")
                
                svgData = ''
                with tempfile.NamedTemporaryFile() as fp:
                    with cairo.SVGSurface(fp.name, WIDTH, HEIGHT) as surface:
                        surface.set_document_unit(cairo.SVG_UNIT_PX)

                        ctx = cairo.Context(surface)
                        ctx.select_font_face(fontName, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                        ctx.set_font_size(SZ)

                        # Origin
                        ctx.translate(WIDTH - MARGIN, HEIGHT - MARGIN)
                        ctx.set_source_rgb(1, 0, 0)
                        ctx.set_line_width(1)
                        ctx.move_to(-WIDTH, 0)
                        ctx.line_to(+WIDTH, 0)
                        ctx.stroke()
                        ctx.move_to(0, -HEIGHT)
                        ctx.line_to(0, +HEIGHT)
                        ctx.stroke()
                    
                        # Cairo drawing
                        breath = reduce(lambda v, e: v + e.xAdvance * EMF, gInfos, 0)
                        curX, curY = -breath, 0
                        for gi in gInfos:
                            drawGlyph(ctx,
                                    gi.gid, curX, curY,
                                    defaultColor,
                                    gi.x * EMF, -gi.y * EMF,
                                    gi.xAdvance * EMF, -gi.yAdvance * EMF,
                                    WIDTH, HEIGHT,
                                    outline=True)

                            curX += gi.xAdvance * EMF
                            curY -= gi.yAdvance * EMF

                    svgData = Path(fp.name).read_text()

                ui.HTML(svgData)

            except Exception as e:
                    showError(f"Error: {e!s}.")
                    if hasattr(e, 'stdout'):
                        showError(f"Error: {e.stdout!s}")