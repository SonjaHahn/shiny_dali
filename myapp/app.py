from shiny import App, render, ui
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from htmltools import br, strong

choices = {"a": "Scatter plot", 
           "b": "Line plot", 
           "c": "Bar plot (vertical)",
           "d": "Bar plot (incl. total)",
           "e": "Bar plot (horizontal)",
           "f": "Heatmap",
           "g": "Pie cart"}

# read in and prepare data
df = pd.read_csv(Path(__file__).parent / 'www/chart.csv', sep = ';')
df.rename(columns = {'Category': 'Year', 'Publications (total)': 'Publications'}, inplace = True)
df = df[df['Year']< 2023]



app_ui = ui.page_fluid(
    ui.panel_title("Which display do you prefer, and why?"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            strong("Try different plots for the same data:"),
            br(),
            ui.input_radio_buttons("x1", "", choices),
            "Underlying data retrieved in June 2023 from ", 
            ui.a({"href": "https://app.dimensions.ai/"}, "app.dimensions.ai"),
            br(),
            ui.img(src="ccby.png",  width="20%"),
            "Sonja Hahn",
        ),
        ui.panel_main(            
            ui.output_plot("my_plot"),
        ),
    ),
)

def server(input, output, session):
    @output
    @render.plot
    def my_plot():
        # title for all plots
        plt.title("Number of scientific publications containing Data Literacy in title or abstract by year")
        # different plots
        if input.x1() == "f":
            x = df.explode('Publications').reset_index()
            plt.imshow(x[['Publications','Year']].to_numpy().astype('float').T)
            plt.colorbar()
            plt.yticks([0,1], ['Publications','Year'])
            return plt.imshow(x[['Publications','Year']].to_numpy().astype('float').T)
        elif input.x1() == "e":
            plt.xlim(0, 8000)
            return plt.barh('Year', 'Publications', data = df)
        elif input.x1() == "g":
            return plt.pie('Publications', labels = 'Year', data=df)
        elif input.x1() == "d":
            df['Sum'] = df['Publications'].cumsum()
            fig, ax = plt.subplots()
            ax.bar('Year', 'Sum', data=df)
            return ax.bar('Year', 'Publications', data=df)
        # last but not least: these share the same y axis
        else:
            plt.ylim(0, 8000)
            if input.x1() == "a":
                return plt.scatter('Year', 'Publications', data = df)
            elif input.x1() == "b":
                return plt.plot('Year', 'Publications', data = df)
            elif input.x1() == "c":
                return plt.bar('Year', 'Publications', data = df)

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)
