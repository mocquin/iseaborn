
import ipywidgets as ipyw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns



palettes = ["pastel", "magma", "ch:.25", "ch:0.95", "Set2", "Set3"]




colors = ["r", "k", "g"]



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
    
    palette_ui = ipyw.Dropdown(
         options=palettes,
         value=palettes[0],
         description='palette:',
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






def barplot(df, cols=[]):
    if len(cols) == 0:
            cols = list(df.columns)
            
    cols_ext = list(cols)
    cols_ext.insert(0, None)
            
    x_ui = ipyw.Dropdown(
         options=cols,
         value=cols[0],
         description='x:',
    )
    
    y_ui = ipyw.Dropdown(
         options=cols,
         value=cols[0],
         description='y:',
    )
    
    hue_ui = ipyw.Dropdown(
        options=cols_ext,
        value=None,
        description="hue:"
    )
    
    estimator_ui = ipyw.Dropdown(
        options={"mean":np.mean,
                 "median":np.median},
        value=np.mean,
        description="estimator"
    )
    
    ci_ui = ipyw.FloatText(
        value=95,
        min=0,
        max=100.0,
        step=0.1,
        description='ci:',
        disabled=False
    )
    
    orient_ui = ipyw.Dropdown(
        options=["h", "v"],
        value="v",
        description="orient:"
    )
    
    color_ui = ipyw.Dropdown(
            options=colors,
            value=colors[0],
            description="color:"
    )
    
    palette_ui = ipyw.Dropdown(
         options=palettes,
         value=palettes[0],
         description='palette:',
    )

    
    errwidth_ui = ipyw.FloatText(
        value=0.75,
        min=0,
        max=1.0,
        step=0.1,
        description='errwidth:',
        disabled=False
    )
    
    capsize_ui = ipyw.FloatText(
        value=0.75,
        min=0,
        max=1.0,
        step=0.1,
        description='capsize:',
        disabled=False
    )    
    
    saturation_ui = ipyw.FloatText(
        value=0.75,
        min=0,
        max=1,
        step=0.01,
        description='saturation:',
        disabled=False
    )
    
    errcolor_ui = ipyw.Dropdown(
            options=colors,
            value=colors[0],
            description="color:"
    )
    
    
    dodge_ui = ipyw.Checkbox(
            value=True,
            description='dodge',
            disabled=False,
            indent=True,
    )
    
    def plot(x='species', 
            y='sepal_length', 
            hue="species",
            estimator=np.mean, # callable that maps vector -> scalar, optional : Statistical function to estimate within each categorical bin.
            ci=95,             # float or “sd” or None,
            orient="v",        # “v” | “h”,
            color="#1CB3B1", # main color, exclusive with palette color matplotlib color, optional
            palette='magma',
            saturation=0.75, 
            errcolor=".26",
            errwidth=None,
            capsize=None,
            dodge=True):
        
        fig, ax = plt.subplots()
        
        sns.barplot(data=df, 
            x=x, 
            y=y, 
            hue=hue,
            estimator=estimator, # callable that maps vector -> scalar, optional : Statistical function to estimate within each categorical bin.
            ci=ci,             # float or “sd” or None,
            orient=orient,         # “v” | “h”,
            color=color, # main color, exclusive with palette color matplotlib color, optional
            palette=palette,
            saturation=saturation, 
            errcolor=errcolor, # matplotlib color
            errwidth=errwidth, # float
            capsize=capsize, # float
            dodge=dodge,
           )
        plt.tight_layout()

        
    inputs_uis = ipyw.VBox(
        [
            x_ui,
            y_ui, 
            hue_ui, 
            estimator_ui, 
            ci_ui, 
            orient_ui, 
            color_ui,
            palette_ui,
            saturation_ui, 
            errcolor_ui, 
            errwidth_ui, 
            capsize_ui, 
            dodge_ui
        ]
    )
    
    out = ipyw.interactive_output(plot, {'x'         :          x_ui, 
                                         "y"         :          y_ui,
                                         "hue"       :        hue_ui,
                                         "estimator" :  estimator_ui,
                                         "ci"        :         ci_ui,
                                         "orient"    :     orient_ui,
                                         "color"     :      color_ui,
                                         "palette"   :    palette_ui,
                                         "saturation": saturation_ui,
                                         "errcolor"  :   errcolor_ui,
                                         "errwidth"  :   errwidth_ui,
                                         "capsize"   :    capsize_ui,
                                         "dodge"     :      dodge_ui,
                                         }
                                 )

    full_ui = ipyw.HBox([
        inputs_uis,
        out,
        ]
    )
    
    return full_ui










def histplot(df, cols=[]):
    if len(cols) == 0:
            cols = list(df.columns)
            
    cols_ext = list(cols)
    cols_ext.insert(0, None)
            
    x_ui = ipyw.Dropdown(
         options=cols_ext,
         value=cols_ext[0],
         description='x:',
    )
    
    y_ui = ipyw.Dropdown(
         options=cols_ext,
         value=cols_ext[0],
         description='y:',
    )
    
    hue_ui = ipyw.Dropdown(
        options=cols_ext,
        value=None,
        description="hue:"
    )
    
    stat_ui = ipyw.Dropdown(
            options=["count", "frequency", "density", "probability"],
            value="count",
            description="stat:"
    )
    
    discrete_ui = ipyw.Checkbox(
            value=True,
            description='discrete:',
            disabled=False,
            indent=True,
    )
    
    cumulative_ui = ipyw.Checkbox(
            value=False,
            description='cumulative:',
            disabled=False,
            indent=True,
    )
    
    common_bins_ui = ipyw.Checkbox(
            value=True,
            description='common_bins:',
            disabled=False,
            indent=True,
    )
    
    common_norm_ui = ipyw.Checkbox(
            value=True,
            description='common_norm:',
            disabled=False,
            indent=True,
    )
    
    multiple_ui = ipyw.Dropdown(
            options=["layer", "dodge", "stack", "fill"],
            value="layer",
            description="multiple:"
    )
    
    element_ui = ipyw.Dropdown(
            options=["bars", "step", "poly"],
            value="bars",
            description="element:"
    )
    
    fill_ui = ipyw.Checkbox(
            value=True,
            description='fill:',
            disabled=False,
            indent=True,
    )
    
    shrink_ui = ipyw.FloatText(
        value=1,
        min=0,
        max=1,
        step=0.01,
        description='shrink:',
        disabled=False
    )    
    
    kde_ui = ipyw.Checkbox(
            value=False,
            description='kde:',
            disabled=False,
            indent=True,
    )        
    
    pmax_ui = ipyw.FloatText(
        value=1,
        min=0,
        max=1,
        step=0.01,
        description='pmax:',
        disabled=False
    )    

    cbar_ui = ipyw.Checkbox(
            value=False,
            description='cbar:',
            disabled=False,
            indent=True,
    )        
    
    palette_ui = ipyw.Dropdown(
         options=palettes,
         value=palettes[0],
         description='palette:',
    )
    
    color_ui = ipyw.Dropdown(
            options=colors,
            value=colors[0],
            description="color:"
    )
    
    legend_ui = ipyw.Checkbox(
            value=False,
            description='legend:',
            disabled=False,
            indent=True,
    )      
        
    def plot(x="sepal_length",
             y="sepal_length",
             hue="None",
             stat="count",           # {“count”, “frequency”, “density”, “probability”}
             #bins="auto",           # str, number, vector, or a pair of such values
             #binwidth=None,         # number or pair of numbers
             discrete=None,          # bool
             cumulative=False,       # bool
             common_bins=True,       # bool
             common_norm=True,       # bool
             multiple="layer",       # {“layer”, “dodge”, “stack”, “fill”}
             element="bars",         # {“bars”, “step”, “poly”}
             fill=True,              # bool
             shrink=1,               # number
             kde=False,              # bool
             pmax=None,              # number or None
             cbar=False,             # bool
             palette=None,           # 
             color=None,             # 
             legend=True):
        
        fig, ax = plt.subplots()
        
        sns.histplot(data=df,
             x=x,
             y=y,
             hue=hue,
             stat=stat,           # {“count”, “frequency”, “density”, “probability”}
             #bins="auto",           # str, number, vector, or a pair of such values
             #binwidth=None,         # number or pair of numbers
             discrete=discrete,          # bool
             cumulative=cumulative,       # bool
             common_bins=common_bins,       # bool
             common_norm=common_norm,       # bool
             multiple=multiple,       # {“layer”, “dodge”, “stack”, “fill”}
             element=element,         # {“bars”, “step”, “poly”}
             fill=fill,              # bool
             shrink=shrink,               # number
             kde=kde,              # bool
             pmax=pmax,              # number or None
             cbar=cbar,             # bool
             palette=palette,           # 
             color=color,             # 
             legend=legend,            # bool
        )

        plt.tight_layout()

        
    inputs_uis = ipyw.VBox(
        [
            x_ui,
            y_ui, 
            hue_ui,
            stat_ui,
            discrete_ui,
            cumulative_ui,
            common_bins_ui,
            common_norm_ui,
            multiple_ui,
            element_ui,
            fill_ui,
            shrink_ui,
            kde_ui,
            pmax_ui,
            cbar_ui,
            palette_ui,
            color_ui,
            legend_ui,
        ]
    )
    
    out = ipyw.interactive_output(plot, {'x'            :           x_ui, 
                                         "y"            :           y_ui,
                                         "hue"          :         hue_ui,
                                         "stat"         :        stat_ui,
                                         "discrete"     :    discrete_ui,
                                         "cumulative"   :  cumulative_ui,
                                         "common_bins"  : common_bins_ui,
                                         "multiple"     :    multiple_ui,
                                         "element"      :     element_ui,
                                         "fill"         :        fill_ui,
                                         "shrink"       :      shrink_ui,
                                         "kde"          :         kde_ui,
                                         "pmax"         :        pmax_ui,
                                         "cbar"         :        cbar_ui,
                                         "palette"      :     palette_ui,
                                         "color"        :       color_ui,
                                         "legend"       :      legend_ui,
                                        } 
                                 )

    full_ui = ipyw.HBox([
        inputs_uis,
        out,
        ]
    )
    
    return full_ui
