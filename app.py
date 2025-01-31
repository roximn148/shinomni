# ******************************************************************************
# Copyright (c) 2025. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
#
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
import shinyswatch
from shiny.express import ui

from .utf import modUtf
from .ttx import modTtx
from .raqm import modRaqm

# UI ***************************************************************************
ui.page_opts(
    window_title='Shinomni',
    theme=shinyswatch.theme.spacelab,
)
ui.tags.style(
    '.progress.shiny-file-input-progress{height: auto;} '
    '.dataframe thead th{text-align:left;text-transform:capitalize;}'
)

ui.h3(
    'Shinomni',
    class_='navbar navbar-expand-lg bg-light',
    style=(
           'padding: 10px;'
           'margin: 10px 0 20px 0;'
           'border-radius: 10px;'
           'border-width: 2px;'),
)


# Panels -----------------------------------------------------------------------
with ui.navset_pill():

    # Text Layout Panel --------------------------------------------------------
    with ui.nav_panel("Raqm"):
        modRaqm('ttx')

    # Font Glyphs Panel --------------------------------------------------------
    with ui.nav_panel("Font Glyphs"):
        modTtx('ttx')

    # UTF Panel -------------------------------------------------------------
    with ui.nav_panel("UTF"):
        modUtf('utf')
