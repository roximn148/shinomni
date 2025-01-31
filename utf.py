# ******************************************************************************
# Copyright (c) 2025. All rights reserved.
# # This work is licensed under the Creative Commons Attribution 4.0
# International License. To view a copy of this license,
# visit # http://creativecommons.org/licenses/by/4.0/.
#
# Author: roximn <roximn148@gmail.com>
# ******************************************************************************
from shiny import reactive
from shiny.express import module, ui, render
import humanize
from collections import Counter
from pathlib import Path

import unicodedataplus as unicodedata
import plotly.express as px
from shiny import reactive
from shiny.express import render, ui
from shinywidgets import render_plotly
import pandas as pd

from .utils import CATEGORIES, BLOCKS, findBlock

# ******************************************************************************
@module
def modUtf(input, output, session):
    # File Info ----------------------------------------------------------------
    @reactive.calc
    def infoHeader():
        info = {'name': '<NO-SELECTION>', 'size': 0}
        files = input.txtFile()
        if files and len(files) >= 1:
            fileData: dict = files[0]
            info['name'] = fileData.get('name', '<???>')
            info['size'] = fileData.get('size', 0)

        header = f'File: {info["name"]}, '\
                 f'size: {humanize.naturalsize(info["size"], binary=True)}'
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
