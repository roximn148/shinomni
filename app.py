from pathlib import Path
import unicodedataplus as unicodedata
from collections import Counter, namedtuple
import re

import humanize
import pandas as pd
import plotly.express as px

from shiny import reactive
from shiny.express import render, ui, input
from shinywidgets import render_plotly
import shinyswatch

from .ttx import modTtx
from .raqm import modRaqm

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
reComment: str = r'^\s*#.*$'
# """Match a complete line of text that start with optional whitespace characters,
# followed by the hash symbol `#`, and then any number of
# non-whitespace characters till the end of the line"""
reBlockRange: str = r'^\s*([0-9A-Fa-f]+)\.\.([0-9A-Fa-f]+)\s*;\s*(.*)\s*$'
# """Match three groups, two hexadecimal codes separated by two dots `..` followed
# by a a semicolon `;` and additional text till end of the line"""

# Read the UNICODE standard blocks text file and extract the ranges and the
# respective block names. Assumes `Blocks.txt` file.
bftxt = Path('Blocks.txt').read_text(encoding='utf8')
lines = [l for l in bftxt.splitlines() if l.strip()]

BLOCKS: list[Block] = []
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
    'Unicode Text Frequency Analyzer (UTF Analyzer)',
    class_='navbar navbar-expand-lg bg-light',
    style=(
           'padding: 10px;'
           'margin: 10px 0 20px 0;'
           'border-radius: 10px;'
           'border-width: 2px;'),
)

# File Info --------------------------------------------------------------------
@reactive.calc
def infoHeader():
    info = {'name': '<NO-SELECTION>', 'size': 0}
    files = input.txtFile()
    if files and len(files) >= 1:
        fileData: dict = files[0]
        info['name'] = fileData.get('name', '<???>')
        info['size'] = fileData.get('size', 0)

    header = f'File: {info["name"]}, size: {humanize.naturalsize(info["size"], binary=True)}'
    return header

# Data -------------------------------------------------------------------------
@reactive.calc
def charDf():
    files = input.txtFile()
    if files is None:
        return None

    if len(files) < 1:
        return None

    fileData: dict = files[0]
    if 'datapath' not in fileData:
        return None

    counts = Counter()
    try:
        with Path(fileData['datapath']).open(mode='r', encoding='utf-8') as file:
            while True:
                chunk = file.read(16*1024)
                if not chunk:
                    break
                counts.update(chunk)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    cdf = pd.DataFrame(counts.items(), columns=['char', 'count'])
    cdf['code'] = cdf['char'].apply(ord)
    cdf['unicode'] = cdf['char'].apply(lambda x: f'U+{ord(x):04X} {unicodedata.name(x, "NO-NAME")}')
    cdf['category'] = cdf['char'].apply(lambda x: unicodedata.category(x))
    cdf['block'] = cdf['code'].apply(lambda x: BLOCKS[findBlock(x)].name)
    cdf['script'] = cdf['char'].apply(lambda x: unicodedata.script(x))

    cdf.sort_values(by='code', ascending=True, inplace=True)
    return cdf

# File Info --------------------------------------------------------------------
@reactive.calc
def infoBody():
    df = charDf()
    if df is not None:
        nChars = len(df)
        totalCount = df['count'].sum()
        nBlocks = df['block'].unique().size
        nScripts = df['script'].unique().size
        nCategories = df['category'].unique().size

        body = f'Selected file contains {humanize.apnumber(nChars)} character(s) '\
            f'with total count of {humanize.intword(totalCount)} ({humanize.intcomma(totalCount)})\n'\
            f'belonging to {humanize.apnumber(nBlocks)} unicode block(s) '\
            f'spanning {humanize.apnumber(nScripts)} script(s) '\
            f'with {humanize.apnumber(nCategories)} different categories.'
    else:
        body = "No processed data."

    return body

# File Selection ---------------------------------------------------------------
with ui.layout_columns(col_widths=(4, 8), fillable=True):
    with ui.card(class_='bg-light border-dark'):
        ui.input_file("txtFile", "Choose a text file to upload:", multiple=False)

    @render.express(inline=True)
    def fileInfoUi():
        with ui.card(class_='bg-light border-dark'):
            ui.card_header(infoHeader())
            infoBody()

# Panels -----------------------------------------------------------------------
with ui.navset_pill():

    # Text Layout Panel --------------------------------------------------------
    with ui.nav_panel("Raqm"):
        modRaqm('ttx')

    # Font Glyphs Panel --------------------------------------------------------
    with ui.nav_panel("Font Glyphs"):
        modTtx('ttx')

    # Counts Panel -------------------------------------------------------------
    with ui.nav_panel("Counts"):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header('Unicode Character Frequency (Least to Most Frequent)')
            @render_plotly
            def chartCounts():
                df = charDf()
                if df is None:
                    return None
                fig = px.bar(df,
                            y='unicode', x='count',
                            orientation='h',
                            log_x=True,
                            text='count',
                            hover_data=['unicode', 'category'],
                            color='category',
                            labels={'unicode': 'Unicode',
                                    'count': 'Frequency',
                                    'category': 'Category'},
                            category_orders={'category': CATEGORIES},
                            color_discrete_sequence=px.colors.qualitative.Plotly)
                fig.update_traces(texttemplate='%{text:,.0f}',
                                textposition='inside',
                                textangle=0)
                fig.update_yaxes(categoryorder='total descending')
                fig.update_layout(height=len(df)*24)
                return fig

    # Code Points Panel --------------------------------------------------------
    with ui.nav_panel("Code Points"):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header('Unicode Character Frequency (Ascending Code Points)')
            @render_plotly
            def chartCodePoints():
                df = charDf()
                if df is None:
                    return None
                fig = px.bar(df,
                            y='unicode', x='count',
                            orientation='h',
                            log_x=True,
                            text='count',
                            hover_data=['unicode', 'category'],
                            color='category',
                            labels={'unicode': 'Unicode',
                                    'count': 'Frequency',
                                    'category': 'Category'},
                            category_orders={'category': CATEGORIES},
                            color_discrete_sequence=px.colors.qualitative.Plotly)
                fig.update_traces(texttemplate='%{text:,.0f}',
                                textposition='inside',
                                textangle=0)
                fig.update_yaxes(categoryorder='category descending')
                fig.update_layout(height=len(df)*24)
                return fig

    # Blocks panel -------------------------------------------------------------
    with ui.nav_panel('Blocks'):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header('Block Counts')
            @render_plotly
            def chartBlockCounts():
                df = charDf()
                if df is None:
                    return None

                blockCounts = df.groupby('block')['count'].sum().reset_index()
                # Filter block names preserving the order of appearance in BLOCKS
                BLOCK_NAMES = [b.name for b in BLOCKS]
                blocks = blockCounts['block'].unique().tolist()
                blocks = [bname for bname in BLOCK_NAMES if bname in blocks]

                fig = px.bar(blockCounts,
                            x='block', y='count',
                            log_y=True,
                            text='count',
                            color='block',
                            labels={'count': 'Frequency',
                                    'block': 'Block'},
                            category_orders={'block': blocks},
                            color_discrete_sequence=px.colors.qualitative.Alphabet)
                fig.update_traces(texttemplate='%{text:,.0f}',
                                textposition='inside',
                                textangle=0)
                fig.update_layout(height=500)
                fig.update_xaxes(categoryorder='total descending')
                return fig

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header('Unicode Character Frequency wrt Blocks')
            @render_plotly
            def chartUnicodeCounts():
                df = charDf()
                if df is None:
                    return None
                fig = px.bar(df,
                            y='unicode', x='count',
                            orientation='h',
                            log_x=True,
                            text='count',
                            hover_data=['unicode', 'block', 'category'],
                            color='block',
                            labels={'unicode': 'Unicode',
                                    'count': 'Frequency',
                                    'category': 'Category',
                                    'block': 'Block'},
                            category_orders={'block': [b.name for b in BLOCKS]},
                            color_discrete_sequence=px.colors.qualitative.Alphabet)
                fig.update_traces(texttemplate='%{text:,.0f}',
                                textposition='inside',
                                textangle=0)
                fig.update_yaxes(categoryorder='category descending')
                fig.update_layout(height=len(df)*24)
                return fig

    # Scripts Panel ------------------------------------------------------------
    with ui.nav_panel("Scripts"):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header("Script Counts")
            @render_plotly
            def chartScriptCounts():
                df = charDf()
                if df is None:
                    return None

                scriptCounts = df.groupby('script')['count'].sum().reset_index()
                scripts = scriptCounts['script'].unique().tolist()
                scripts.sort()

                fig = px.bar(scriptCounts,
                            x='script', y='count',
                            log_y=True,
                            text='count',
                            color='script',
                            labels={'count': 'Frequency',
                                    'script': 'Script'},
                            category_orders={'script': scripts},
                            color_discrete_sequence=px.colors.qualitative.Alphabet)
                fig.update_traces(texttemplate='%{text:,.0f}',
                                textposition='inside',
                                textangle=0)
                fig.update_layout(height=500)
                fig.update_xaxes(categoryorder='total descending')
                return fig

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header("Unicode Character Frequency wrt Script")
            @render_plotly
            def chartScripts():
                df = charDf()
                if df is None:
                    return None

                SCRIPTS: list[str] = (df['script']
                                    .dropna()
                                    .sort_values()
                                    .unique()
                                    .tolist())

                fig = px.bar(df,
                            y='unicode', x='count',
                            orientation='h',
                            title='Unicode Character Frequency',
                            log_x=True,
                            text='count',
                            hover_data=['unicode', 'script', 'block', 'category'],
                            color='script',
                            labels={
                                'unicode': 'Unicode',
                                'count': 'Frequency',
                                'category': 'Category',
                                'block': 'Block',
                                'script': 'Script'},
                            category_orders={'script': SCRIPTS},
                            color_discrete_sequence=px.colors.qualitative.Alphabet)
                fig.update_traces(texttemplate='%{text:,.0f}',
                                textposition='inside',
                                textangle=0)
                fig.update_yaxes(categoryorder='category descending')
                fig.update_layout(height=len(df)*24)

                return fig

    # Normalized CDF -----------------------------------------------------------
    with ui.nav_panel("Normalized CFD"):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            ui.card_header('Normalized Cumulative Frequency Distribution')
            @render_plotly
            def chartEcdf():
                df = charDf()
                if df is None:
                    return None

                df = df.sort_values(by='count', ascending=True)
                # Calculate cumulative counts
                df['CumCount'] = df['count'].cumsum()
                total = df['count'].sum()
                df['nCumFreq'] = df['CumCount'] / total

                # Plot using Plotly Express with step-line
                fig = px.line(df,
                            y='unicode', x='nCumFreq',
                            labels={'Element': 'Element',
                                    'CumCount': 'Cumulative Count',
                                    'nCumFreq': 'Normalized Cumulative Frequency'},
                            line_shape='vh')
                fig.update_xaxes(range=[0, 1.1])
                fig.update_layout(height=len(df)*24)

                for percentile in [round(i * 0.1, 1) for i in range(0, 11, 2)]:
                    fig.add_hline(y=percentile*len(df)-1,
                                line=dict(color='green', dash='dot', width=2),
                                annotation_text=f'{percentile*100}%')
                    fig.add_vline(x=percentile,
                                line=dict(color='red', dash='dash', width=1),
                                annotation_text=f'{percentile*100}%')

                return fig

    # Table Panel --------------------------------------------------------------
    with ui.nav_panel("Table"):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            @render.table(classes='table table-hover')
            def tablePanel():
                return charDf()

    # Dataframe Panel ----------------------------------------------------------
    with ui.nav_panel("Data frame"):

        # ----------------------------------------------------------------------
        with ui.card(fill=True, class_='border-light'):
            @render.data_frame
            def dataframePanel():
                df = charDf()
                if df is None:
                    return None
                return render.DataTable(df, selection_mode="rows")
