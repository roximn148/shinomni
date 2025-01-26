# Shinomni
Shinomni (combination of *Shiny* and *Omni*) is `Shiny` application aggregating a few multi-purpose utilities.

## Features

### UTF Analyzer
- Analyses UTF8 text files and provides statistical analysis of the usage of various unicode characters, their categories, blocks and scripts.

### Font Analyzer
- Renders and displays glyphs of selected font in order of appearance in font.

### Raqm Layout
- Render given text with Raqm layout engine using specified font, direction and language.


## Setup
1. Install `Shiny Server` by following the instructions [here](https://shiny.posit.co/py/docs/deploy-on-prem.html#deploy-to-shiny-server-open-source). It also details how to add `shinomni` to the server.
2. Clone this repository to your local machine using `git clone https://github.com/roximn148/shinomni`
3. Create a virtual environment in the project directory and activate it
4. Install the required Python dependencies using `pip install -r pyproject.toml`

## Usage
Once the installation is complete, you can access the application by opening your web browser and navigating to `http://localhost:3838/`.
