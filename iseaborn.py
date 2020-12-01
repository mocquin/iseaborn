
import ipywidgets as ipyw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns



palettes = ["pastel", "magma", "ch:.25", "ch:0.95", "Set2", "Set3"]

def countplot(df, cols=[]):
    if len(cols) == 0:
            cols = list(df.columns)
            
    cols_ext = list(cols)
    cols_ext.insert(0, None)
            
    x_ui = ipyw.Dropdown(
         options=cols,
         value=cols[0],
         description='x:',
    )
    
    palette_ui = ipyw.Dropdown(
         options=palettes,
         value=palettes[0],
         description='palette:',
    )
    
    
    hue_ui = ipyw.Dropdown(
        options=cols_ext,
        value=None,
        description="hue",
        
    )
    
    dodge_ui = ipyw.Checkbox(
            value=True,
            description='dodge',
            disabled=False,
            indent=True,
        )
    
    inputs_uis = ipyw.VBox([
        x_ui,
        hue_ui,
        dodge_ui,
        palette_ui,
        ]
    )
    
    
    def plot(x, hue,
             dodge=True,
             palette="ch:.25"):
        sns.catplot(kind="count", data=df, 
                x=x, 
                hue=hue,
                palette=palette ,
                dodge=dodge
               )

        

    out = ipyw.interactive_output(plot, {'x': x_ui,
                                         "hue":hue_ui,
                                         "dodge":dodge_ui,
                                         "palette":palette_ui,
                                         }
                                 )
    
    full_ui = ipyw.HBox([
        inputs_uis,
        out,
        ]
    )
    
    return full_ui





def heatmap(df, cols=[]):
    if len(cols) == 0:
            cols = list(df.columns)

    cols_ui  = ipyw.SelectMultiple(
        options=cols,
        description="Select ctrl",
        )
    
    annot_ui = ipyw.Checkbox(
            value=True,
            description='annot',
            disabled=False,
            indent=False,
        )
    cbar_ui = ipyw.Checkbox(
            value=True,
            description='cbar',
            disabled=False,
            indent=False,
        )
    square_ui = ipyw.Checkbox(
            value=False,
            description='square',
            disabled=False,
            indent=False,
        )
    
    inputs_uis = ipyw.VBox([
        cols_ui,
        annot_ui,
        cbar_ui,
        square_ui,
        ]
    )
    
    def plot(cols, annot=True, cbar=True, square=False):
        fig, ax = plt.subplots()

        cols = list(cols)
        if len(cols) == 0:
            cols = list(df.columns)
        sns.heatmap(
            df[cols].corr(),
            vmin=-1,
            vmax=1,
            annot=annot,
            linewidth=0.5, # linewidth separating cells
            linecolor="k", # color of lines separating cells
            cbar=cbar,     # add a colorbar
            square=square,  # enforce square cells
            ax=ax
        )
        plt.tight_layout()

    
    out = ipyw.interactive_output(plot, {'cols': cols_ui,
                                         "annot":annot_ui,
                                         "cbar": cbar_ui,
                                         "square":square_ui,
                                         }
                                 )

    full_ui = ipyw.HBox([
        inputs_uis,
        out,
        ]
    )
    
    return full_ui



def pairplot(df, cols=[]):
    if len(cols) == 0:
            cols = list(df.columns)

    cols_ext = list(cols)
    cols_ext.insert(0, None)
            
    cols_ui  = ipyw.SelectMultiple(
        options=cols,
        description="Select ctrl",
        )
    
    kind_ui = ipyw.Dropdown(
            options=["scatter", "kde", "hist", "reg"],
            value="scatter",
            description='kind:',
        )
    
    hue_ui = ipyw.Dropdown(
        options=cols_ext,
        value=None,
        description="hue"
    )
    
    diag_kind_ui = ipyw.Dropdown(
            options=[("auto","auto"), 
                     ("hist","hist"),
                     ("kde","kde"),
                     ("None",None)],
            value="auto",
            description='diag_kind:',
        )
    
    corner_ui = ipyw.Checkbox(
        value=True,
        description='corner',
    )
    
    
    inputs_uis = ipyw.VBox([
        cols_ui,
        kind_ui,
        hue_ui,
        diag_kind_ui,
        corner_ui,
        ]
    )
    
    def plot(cols,
             kind="scatter",
             hue=None,
             diag_kind="auto",
             corner=True,
            ):
        #fig, ax = plt.subplots()

        cols = list(cols)
        if len(cols) == 0:
            cols = list(df.columns)
        
        sns.pairplot(
             data=df[cols], 
             kind=kind,                              #plot-kind in cross cells : {‘scatter’, ‘kde’, ‘hist’, ‘reg’}
             #vars=,
             #x_vars=iris_num_cols, # restrict variables on xaxis
             #y_vars=iris_num_cols, # restrict variables on yaxis
             hue=hue,
             diag_kind=diag_kind,                    # plot-kind on diagonal cells : "auto", "hist", "kde", None
             height=1.5,                               # height of cell
             aspect=1,                               # width wrt heigth
             palette="Set2",
             corner=corner,    # low-left-triangle plots only : True/false
            )
        plt.tight_layout()

    
    out = ipyw.interactive_output(plot, {'cols': cols_ui,
                                         "kind":kind_ui,
                                         "hue": hue_ui,
                                         "diag_kind":diag_kind_ui,
                                         "corner":corner_ui
                                         }
                                 )

    full_ui = ipyw.HBox([
        inputs_uis,
        out,
        ]
    )
    
    return full_ui

