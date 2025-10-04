from dataclasses import dataclass
from enum import Enum, auto

import shinyswatch
from shiny import reactive
from shiny.express import render, ui, input

# Enums ************************************************************************
class Compositions(Enum):
    Unspecified = auto()
    Cystic = auto()
    Spongiform = auto()
    Mixed = auto()
    Solid = auto()
    Indeterminate = auto()

class Echogenicities(Enum):
    Unspecified = auto()
    Anechoic = auto()
    Hyperechoic = auto()
    Isoechoic = auto()
    Hypoechoic = auto()
    VeryHypoechoic = auto()
    Indeterminate = auto()

class Shapes(Enum):
    Unspecified = auto()
    WiderThanTall = auto()
    TallerThanWide = auto()

class Margins(Enum):
    Unspecified = auto()
    Smooth = auto()
    IllDefined = auto()
    LobulatedIrregular = auto()
    ExtraThyroidal = auto()
    Indeterminate = auto()

class Foci(Enum):
    Unspecified = auto()
    NoFoci = auto()
    LargeCometTail  = auto()
    Macrocalcifications = auto()
    RimCalcifications = auto()
    PunctateFoci = auto()


# ******************************************************************************
# @dataclass
# class NoduleFeatures:
#     laterality: str = ''
#     position: str = ''
#     size: str = ''
#     composition: Compositions = Compositions.Unspecified,
#     echogenicity: Echogenicities = Echogenicities.Unspecified
#     shape: Shapes = Shapes.Unspecified
#     margin: Margins = Margins.Unspecified
#     foci: Foci = Foci.Unspecified

# noduleFeatures = NoduleFeatures()

# UI ***************************************************************************
ui.page_opts(
    window_title='TIRADS Calculator',
    theme=shinyswatch.theme.spacelab,
)
ui.tags.style(
    '.progress.shiny-file-input-progress{height: auto;} '
    '.dataframe thead th{text-align:left;text-transform:capitalize;}'
)

ui.h3(
    'TIRADS Calculator',
    class_='navbar navbar-expand-lg bg-light',
    style=(
           'padding: 10px;'
           'margin: 10px 0 20px 0;'
           'border-radius: 10px;'
           'border-width: 2px;'),
)

# Location and Size ------------------------------------------------------------
trLocations = {
    "rightUpper": ui.span("Right Upper"),
    "rightMiddle": ui.span("Right Middle"),
    "rightLower": ui.span("Right Lower"),
    "isthmus": ui.span("Isthmus"),
    "leftUpper": ui.span("Left Upper"),
    "leftMiddle": ui.span("Left Middle"),
    "leftLower": ui.span("Left Lower"),
}

with ui.layout_columns():
    with ui.card(fill=True, class_='border-dark'):
        ui.card_header('1. Location')
        with ui.layout_columns():
            with ui.card(fill=True, class_='border-light'):
                ui.card_header('Laterality')
                ui.input_radio_buttons(
                    id="rbxLaterality",
                    label="",
                    choices={
                            "right": ui.span("Right Lobe"),
                            "isthmus": ui.span("Isthmus"),
                            "left": ui.span("Left Lobe"),
                    },
                    inline=False,
                )
            with ui.card(fill=True, class_='border-light'):
                ui.card_header('Position')
                ui.input_radio_buttons(
                    id="rbxPosition",
                    label="",
                    choices={
                        "upper": ui.span("Upper"),
                        "middle": ui.span("Middle"),
                        "lower": ui.span("Lower"),
                        "notApplicable": ui.span("Not Applicable"),
                    },
                    inline=False,
                )

    with ui.card(fill=True, class_='border-dark'):
        ui.card_header('2. Size')
        ui.input_slider(
            "noduleSize",
            "Size (cm)",
            min=0.0, max=20.0, step=0.1,
            value=0.0, ticks=True, post=" cm",
            width="100%"
        )
        @render.text
        def value7():
            return f"Largest dimesion: {input.noduleSize()} cm"

# Composition ------------------------------------------------------------------
composition = reactive.value(Compositions.Unspecified)

with ui.card(fill=True, class_='border-dark'):
    ui.card_header('3. Composition')
    with ui.layout_columns():

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Cystic<br>Almost Completely Cystic'), style="text-align:center;"))
            @render.ui
            def renderCompCystic():
                return ui.input_action_button(
                    "btnCompCystic",
                    label=ui.img(src="images/TIRADS_cystic.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if composition() == Compositions.Cystic
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Spongiform<br><br>'), style="text-align:center;"))

            @render.ui
            def renderCompSpongiform():
                return ui.input_action_button(
                    "btnCompSpongiform",
                    label=ui.img(src="images/TIRADS_spongiform.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if composition() == Compositions.Spongiform
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Mixed Cystic & Solid<br><br>'), style="text-align:center;"))
            @render.ui
            def renderCompMixed():
                return ui.input_action_button(
                    "btnCompMixed",
                    label=ui.img(src="images/TIRADS_mixed.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if composition() == Compositions.Mixed
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Solid</br>Almost Completely Solid'), style="text-align:center;"))
            @render.ui
            def renderCompSolid():
                return ui.input_action_button(
                    "btnCompSolid",
                    label=ui.img(src="images/TIRADS_almostSolid.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if composition() == Compositions.Solid
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Indeterminate</br>(due to calcification)'), style="text-align:center;"))
            @render.ui
            def renderCompIndeterminate():
                return ui.input_action_button(
                    "btnCompIndeterminate",
                    label=ui.img(src="images/question.png",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if composition() == Compositions.Indeterminate
                            else 'btn btn-light'),
                )

btnComps = [
    "btnCompCystic",
    "btnCompSpongiform",
    "btnCompMixed",
    "btnCompSolid",
    "btnCompIndeterminate",
]

@render.ui
@reactive.event(input.btnCompCystic)
def onCompCysticClick():
    ui.update_action_button("btnCompCystic",
                            icon=ui.span("+0", class_="badge bg-success"))
    btns = btnComps[:]
    btns.remove("btnCompCystic")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    composition.set(Compositions.Cystic)

@render.ui
@reactive.event(input.btnCompSpongiform)
def onCompSpongiformClick():
    ui.update_action_button("btnCompSpongiform",
                            icon=ui.span("+0", class_="badge bg-success"))
    btns = btnComps[:]
    btns.remove("btnCompSpongiform")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    composition.set(Compositions.Spongiform)

@render.ui
@reactive.event(input.btnCompMixed)
def onCompMixedClick():
    ui.update_action_button("btnCompMixed",
                            icon=ui.span("+1", class_="badge bg-warning"))
    btns = btnComps[:]
    btns.remove("btnCompMixed")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    composition.set(Compositions.Mixed)

@render.ui
@reactive.event(input.btnCompSolid)
def onCompSolidClick():
    ui.update_action_button("btnCompSolid",
                            icon=ui.span("+2", class_="badge bg-danger"))
    btns = btnComps[:]
    btns.remove("btnCompSolid")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    composition.set(Compositions.Solid)

@render.ui
@reactive.event(input.btnCompIndeterminate)
def onCompIndeterminateClick():
    ui.update_action_button("btnCompIndeterminate",
                            icon=ui.span("+2", class_="badge bg-danger"))
    btns = btnComps[:]
    btns.remove("btnCompIndeterminate")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    composition.set(Compositions.Indeterminate)

# Echogenicity -----------------------------------------------------------------
echogenicity = reactive.Value(Echogenicities.Unspecified)

with ui.card(fill=True, class_='border-dark'):
    ui.card_header('4. Echogenicity')
    with ui.layout_columns():

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Anechoic<br>Almost Completely Cystic'), style="text-align:center;"))
            @render.ui
            def renderEchoAnechoic():
                return ui.input_action_button(
                    "btnEchoAnechoic",
                    label=ui.img(src="images/TIRADS_anechoic.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if echogenicity() == Echogenicities.Anechoic
                            else 'btn btn-light'),
                    height="220px",
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Isoechoic<br><br>'), style="text-align:center;"))
            @render.ui
            def renderEchoIsoechoic():
                return ui.input_action_button(
                    "btnEchoIsoechoic",
                    label=ui.img(src="images/TIRADS_isoechoic.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if echogenicity() == Echogenicities.Isoechoic
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Hyperechoic<br><br>'), style="text-align:center;"))
            @render.ui
            def renderEchoHyperechoic():
                return ui.input_action_button(
                    "btnEchoHyperechoic",
                    label=ui.img(src="images/TIRADS_hyperechoic.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if echogenicity() == Echogenicities.Hyperechoic
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Hypoechoic<br><br>'), style="text-align:center;"))
            @render.ui
            def renderEchoHypoechoic():
                return ui.input_action_button(
                    "btnEchoHypoechoic",
                    label=ui.img(src="images/TIRADS_veryHypoechoic.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if echogenicity() == Echogenicities.Hypoechoic
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Very Hypoechoic<br><br>'), style="text-align:center;"))
            @render.ui
            def renderEchoVeryHypoechoic():
                return ui.input_action_button(
                    "btnEchoVeryHypoechoic",
                    label=ui.img(src="images/TIRADS_veryHypoechoic.jpg"
                                 , width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if echogenicity() == Echogenicities.VeryHypoechoic
                            else 'btn btn-light'),
                )


btnEchos = [
    "btnEchoAnechoic",
    "btnEchoIsoechoic",
    "btnEchoHyperechoic",
    "btnEchoHypoechoic",
    "btnEchoVeryHypoechoic",
]

@render.ui
@reactive.event(input.btnEchoAnechoic)
def onEchoAnechoicClick():
    ui.update_action_button("btnEchoAnechoic",
                            icon=ui.span("+0",class_="badge bg-success"))
    btns = btnEchos[:]
    btns.remove("btnEchoAnechoic")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    echogenicity.set(Echogenicities.Anechoic)

@render.ui
@reactive.event(input.btnEchoIsoechoic)
def onEchoIsoechoicClick():
    ui.update_action_button("btnEchoIsoechoic",
                            icon=ui.span("+1", class_="badge bg-info"))
    btns = btnEchos[:]
    btns.remove("btnEchoIsoechoic")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    echogenicity.set(Echogenicities.Isoechoic)

@render.ui
@reactive.event(input.btnEchoHyperechoic)
def onEchoHyperechoicClick():
    ui.update_action_button("btnEchoHyperechoic",
                            icon=ui.span("+1", class_="badge bg-info"))
    btns = btnEchos[:]
    btns.remove("btnEchoHyperechoic")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    echogenicity.set(Echogenicities.Hyperechoic)

@render.ui
@reactive.event(input.btnEchoHypoechoic)
def onEchoHypoechoicClick():
    ui.update_action_button("btnEchoHypoechoic",
                            icon=ui.span("+2", class_="badge bg-warning"))
    btns = btnEchos[:]
    btns.remove("btnEchoHypoechoic")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    echogenicity.set(Echogenicities.Hypoechoic)

@render.ui
@reactive.event(input.btnEchoVeryHypoechoic)
def onEchoVeryHypoechoicClick():
    ui.update_action_button("btnEchoVeryHypoechoic",
                            icon=ui.span("+3", class_="badge bg-danger"))
    btns = btnEchos[:]
    btns.remove("btnEchoVeryHypoechoic")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    echogenicity.set(Echogenicities.VeryHypoechoic)


# Shape ------------------------------------------------------------------------
shape = reactive.Value(Shapes.Unspecified)

with ui.card(fill=True, class_='border-dark'):
    ui.card_header('5. Shape')
    with ui.layout_column_wrap(width=1/10, fill=False, fillable=False):
        with ui.card(fill=False, class_='border-light'):
            ui.card_header(ui.div('Wider than tall', style="text-align:center;"))
            @render.ui
            def renderShapeWider():
                return ui.input_action_button(
                    "btnShapeWider",
                    label=ui.img(src="images/TIRADS_wider.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if shape() == Shapes.WiderThanTall
                            else 'btn btn-light')
                )

        with ui.card(fill=False, class_='border-light'):
            ui.card_header(ui.div('Taller than Wide', style="text-align:center;"))
            @render.ui
            def renderShapeTaller():
                return ui.input_action_button(
                    "btnShapeTaller",
                    label=ui.img(src="images/TIRADS_taller.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if shape() == Shapes.TallerThanWide
                            else 'btn btn-light'),
                )

@render.ui
@reactive.event(input.btnShapeWider)
def onShapeWiderClick():
    ui.update_action_button("btnShapeWider",
                            icon=ui.span("+0",class_="badge bg-success"))
    ui.update_action_button("btnShapeTaller", icon="\u003F")
    shape.set(Shapes.WiderThanTall)

@render.ui
@reactive.event(input.btnShapeTaller)
def onShapeTallerClick():
    ui.update_action_button("btnShapeTaller",
                            icon=ui.span("+3", class_="badge bg-danger"))
    ui.update_action_button("btnShapeWider", icon="\u003F")
    shape.set(Shapes.TallerThanWide)


# Margins -----------------------------------------------------------------
margin = reactive.Value(Margins.Unspecified)

with ui.card(fill=True, class_='border-dark'):
    ui.card_header('6. Margins')
    with ui.layout_columns():

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Smooth'), style="text-align:center;"))
            @render.ui
            def renderMarginSmooth():
                return ui.input_action_button(
                    "btnMarginSmooth",
                    label=ui.img(src="images/TIRADS_smooth.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if margin() == Margins.Smooth
                            else 'btn btn-light'),
                    height="220px",
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Ill-Defined'), style="text-align:center;"))
            @render.ui
            def renderMarginIllDefined():
                return ui.input_action_button(
                    "btnMarginIllDefined",
                    label=ui.img(src="images/TIRADS_illdefined.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if margin() == Margins.IllDefined
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Lobulated/Irregular'), style="text-align:center;"))
            @render.ui
            def renderMarginLobulated():
                return ui.input_action_button(
                    "btnMarginLobulated",
                    label=ui.img(src="images/TIRADS_irregular.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if margin() == Margins.LobulatedIrregular
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Extrathyroidal Extension'), style="text-align:center;"))
            @render.ui
            def renderMarginExtraThyroidal():
                return ui.input_action_button(
                    "btnMarginExtraThyroidal",
                    label=ui.img(src="images/TIRADS_extraThyroid.jpg",
                                 width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if margin() == Margins.ExtraThyroidal
                            else 'btn btn-light'),
                )

        with ui.card(fill=True, class_='border-light'):
            ui.card_header(ui.div(ui.HTML('Indeterminate'), style="text-align:center;"))
            @render.ui
            def renderMarginIndeterminate():
                return ui.input_action_button(
                    "btnMarginIndeterminate",
                    label=ui.img(src="images/question.png"
                                 , width="175px", height="175px"),
                    icon="\u003F",
                    class_=('btn btn-primary'
                            if margin() == Margins.Indeterminate
                            else 'btn btn-light'),
                )


btnMargins = [
    "btnMarginSmooth",
    "btnMarginIllDefined",
    "btnMarginLobulated",
    "btnMarginExtraThyroidal",
    "btnMarginIndeterminate",
]

@render.ui
@reactive.event(input.btnMarginSmooth)
def onMarginSmoothClick():
    ui.update_action_button("btnMarginSmooth",
                            icon=ui.span("+0",class_="badge bg-success"))
    btns = btnMargins[:]
    btns.remove("btnMarginSmooth")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    margin.set(Margins.Smooth)

@render.ui
@reactive.event(input.btnMarginIllDefined)
def onMarginIllDefinedClick():
    ui.update_action_button("btnMarginIllDefined",
                            icon=ui.span("+0", class_="badge bg-success"))
    btns = btnMargins[:]
    btns.remove("btnMarginIllDefined")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    margin.set(Margins.IllDefined)

@render.ui
@reactive.event(input.btnMarginLobulated)
def onMarginLobulatedClick():
    ui.update_action_button("btnMarginLobulated",
                            icon=ui.span("+2", class_="badge bg-warning"))
    btns = btnMargins[:]
    btns.remove("btnMarginLobulated")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    margin.set(Margins.LobulatedIrregular)

@render.ui
@reactive.event(input.btnMarginExtraThyroidal)
def onMarginExtraThyroidalClick():
    ui.update_action_button("btnMarginExtraThyroidal",
                            icon=ui.span("+3", class_="badge bg-danger"))
    btns = btnMargins[:]
    btns.remove("btnMarginExtraThyroidal")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    margin.set(Margins.ExtraThyroidal)

@render.ui
@reactive.event(input.btnMarginIndeterminate)
def onMarginIndeterminateClick():
    ui.update_action_button("btnMarginIndeterminate",
                            icon=ui.span("+0", class_="badge bg-success"))
    btns = btnMargins[:]
    btns.remove("btnMarginIndeterminate")
    for btn in btns:
        ui.update_action_button(btn, icon="\u003F")
    margin.set(Margins.Indeterminate)
