import ipywidgets as widgets
import seaborn
import pandas as pd

# see https://matplotlib.org/3.1.1/gallery/color/colormap_reference.html
PALETTES = [
    "deep", "muted", "bright", "pastel", "dark", "colorblind",
    "pastel", "magma", "ch:.25", "ch:0.95", "Set2", "Set3",
    "husl", "hsl",
        'viridis', 'plasma', 'inferno', 'magma', 'cividis',
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper',
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
        'twilight', 'twilight_shifted', 'hsv',
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c',
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'
            ]



class SeabornWidgetDispenser(object):
    """
    Example
    -------
    >>> import seaborn as sns
    >>> from seaborn_widgets_map import WidgetDispenser
    >>> iris = sns.load_dataset("iris")
    >>> iris_widgets = WidgetDispenser(iris)
    >>> iris_widgets("a")
    # returns a Dropdown widget containing the cols names
    """
    
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError
        self.df = df
        
        col_list = list(df)
        col_list_ext = list(col_list)
        col_list_ext.append(None)
        col_list_as_dict = {str(k):k for k in col_list}
        col_list_as_dict_ext = dict(col_list_as_dict)
        col_list_as_dict_ext["None"] = None
        col_tuples = [(col, list(df[col])) for col in col_list]
        
        # dict mapping a param name, and a tuple with the widget, and the args for the widget
        # use as : widget, kwargs = widget_map["x"]
        # x_widget = widget(**kwargs)
        self.widget_map = {
            
        "a"                 : (widgets.Dropdown,             {"options":col_tuples                                                                 }),
        "a_select"          : (widgets.SelectMultiple,       {"options":col_list, "description":"Column selector"                                  }),
        "a_select_ext"      : (widgets.SelectMultiple,       {"options":col_list_ext                                                               }),
        "alpha"             : (widgets.FloatSlider,          {"min":0.0, "max":1.0, "step":0.05                                                    }),
        "annot"             : (widgets.Checkbox,             {                                                                                     }),
        "aspect"            : (widgets.FloatText,            {"value":1, "step":0.05                                                               }),
        "axlabel"           : (widgets.Text,                 {                                                                                     }),
        "bins"              : (widgets.IntText,              {"value":10                                                                           }),
        "bw"                : (widgets.Dropdown,             {"options":["scott", "silverman"]                                                     }),
        "capsize"           : (widgets.FloatText,            {"value":1.0                                                                          }),
        "cbar"              : (widgets.Checkbox,             {                                                                                     }),
        "cbar"              : (widgets.Checkbox,             {                                                                                     }),
        "cbar_ax"           : (widgets.Checkbox,             {                                                                                     }),
        "center"            : (widgets.FloatText,            {"value":1.0                                                                          }),
        "ci"                : (widgets.FloatSlider,          {"min":0, "max":100, "value":95, "step":0.1                                           }),
        "cmap"              : (widgets.Text,                 {"value":"viridis"                                                                    }),
        "col"               : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "col_wrap"          : (widgets.IntText,              {"value":10                                                                           }),
        "color"             : (widgets.Text,                 {"value":"g"                                                                          }),
        "cumulative"        : (widgets.Checkbox,             {                                                                                     }),
        "cut"               : (widgets.FloatText,            {"value":1.0                                                                          }),
        "data"              : (widgets.Dropdown,             {"options":col_tuples                                                                 }),
        "data2"             : (widgets.Dropdown,             {"options":col_tuples                                                                 }),
        "diag_kind"         : (widgets.Dropdown,             {"options":["auto", "hist", "kde"]                                                    }),
        "dropna"            : (widgets.Checkbox,             {                                                                                     }),
        "edgecolor"         : (widgets.Text,                 {"value":"gray"                                                                       }),
        "err_style"         : (widgets.Dropdown,             {"options":["band", "bars"]                                                           }),
        "errwidth"          : (widgets.FloatText,            {"value":1.0                                                                          }),
        "fit_reg"           : (widgets.Checkbox,             {                                                                                     }),
        "fliersize"         : (widgets.FloatText,            {"value":1.0                                                                          }),
        "fmt"               : (widgets.Text,                 {"value":".2g"                                                                        }),
        "gridsize"          : (widgets.IntText,              {"value":100                                                                          }),
        "height"            : (widgets.FloatText,            {"value":5                                                                            }),
        "hist"              : (widgets.Checkbox,             {                                                                                     }),
        "hue"               : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "inner"             : (widgets.Dropdown,             {"options":["box", "quartile", "point", "stick"]                                      }),
        "jitter"            : (widgets.Checkbox,             {                                                                                     }),
        "join"              : (widgets.Checkbox,             {                                                                                     }),
        "k_depth"           : (widgets.Dropdown,             {"options":["proportion", "tukey", "trustworthy"]                                     }),
        "kde"               : (widgets.Checkbox,             {                                                                                     }),
        "kernel"            : (widgets.Dropdown,             {"options":['gau', 'cos', 'biw', 'epa', 'tri', 'triw']                                }),
        "kind_catplot"      : (widgets.Dropdown,             {"options":["point", "bar", "strip", "swarm", "box", "violin", "boxen"]               }),
        "kind_jointplot"    : (widgets.Dropdown,             {"options":["scatter", "reg", "resid", "kde", "hex"]                                  }),
        "kind_pairplot"     : (widgets.Dropdown,             {"options":["scatter", "reg"]                                                         }),
        "kind_relplot"      : (widgets.Dropdown,             {"options":["scatter", "line"]                                                        }),
        "label"             : (widgets.Text,                 {                                                                                     }),
        "legend"            : (widgets.Dropdown,             {"options":{"brief": "brief", "full":"full", "False": False}                          }),
        "legend_out"        : (widgets.Checkbox,             {                                                                                     }),
        "linecolor"         : (widgets.Text,                 {"value":"white"                                                                      }),
        "linewidth"         : (widgets.FloatText,            {"value":1.0                                                                          }),
        "linewidths"        : (widgets.FloatText,            {"value":0.0, "step":0.01                                                             }),
        "logistic"          : (widgets.Checkbox,             {                                                                                     }),
        "logx"              : (widgets.Checkbox,             {                                                                                     }),
        "lowess"            : (widgets.Checkbox,             {                                                                                     }),
        "margin_titles"     : (widgets.Checkbox,             {                                                                                     }),
        "marker"            : (widgets.Dropdown,             {"options":['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']}),
        "n_boot"            : (widgets.IntText,              {"value":1000                                                                         }),
        "norm_hist"         : (widgets.Checkbox,             {                                                                                     }),
        "notch"             : (widgets.Checkbox,             {                                                                                     }),
        "order_regression"  : (widgets.IntText,              {"value":1                                                                            }),
        "orient"            : (widgets.Dropdown,             {"options":["v", "h"]                                                                 }),
        "outlier_prop"      : (widgets.FloatSlider,          {"min":0.0, "max":1.0, "step":0.001, "value":0.007                                    }),
        "palette"           : (widgets.Dropdown,             {"options":PALETTES                                                                   }),
        "ratio"             : (widgets.IntText,              {"value":5                                                                            }),
        "robust"            : (widgets.Checkbox,             {                                                                                     }),
        "row"               : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "rug"               : (widgets.Checkbox,             {                                                                                     }),
        "saturation"        : (widgets.FloatSlider,          {"min":0.0, "max":1.0, "step":0.05, "value":1.0                                       }),
        "scale_boxenplot"   : (widgets.Dropdown,             {"options":["linear", "exponential", "area"]                                          }),
        "scale_float"       : (widgets.FloatText,            {"value":1.0                                                                          }),
        "scale_hue"         : (widgets.Checkbox,             {                                                                                     }),
        "scale_violinplot"  : (widgets.Dropdown,             {"options":["area", "count", "width"]                                                 }),
        "scatter"           : (widgets.Checkbox,             {                                                                                     }),
        "shade"             : (widgets.Checkbox,             {                                                                                     }),
        "shade_lowest"      : (widgets.Checkbox,             {                                                                                     }),
        "sharex"            : (widgets.Dropdown,             {"options":{"True": True, "col": "col", "row": "row"}                                 }),
        "sharey"            : (widgets.Dropdown,             {"options":{"True": True, "col": "col", "row": "row"}                                 }),
        "size_float"        : (widgets.FloatText,            {"value":1.0                                                                          }),
        "size_vector"       : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "sort"              : (widgets.Checkbox,             {                                                                                     }),
        "space"             : (widgets.FloatText,            {"value":.2                                                                           }),
        "split"             : (widgets.Checkbox,             {                                                                                     }),
        "square"            : (widgets.Checkbox,             {                                                                                     }),
        "style"             : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "truncate"          : (widgets.Checkbox,             {                                                                                     }),
        "units"             : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "vertical"          : (widgets.Checkbox,             {                                                                                     }),
        "vmax"              : (widgets.FloatText,            {"value":1.0, "step":0.1                                                              }),
        "vmin"              : (widgets.FloatText,            {"value":0.0, "step":0.1                                                              }),
        "whis"              : (widgets.FloatText,            {"value":1.0                                                                          }),
        "width"             : (widgets.FloatText,            {"value":1.0                                                                          }),
        "x"                 : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "x_bins"            : (widgets.IntText,              {"value":10                                                                           }),
        "x_ci"              : (widgets.IntSlider,            {"min":0, "max":100, "value":95                                                       }),
        "x_jitter"          : (widgets.FloatText,            {"value":.1                                                                           }),
        "x_partial"         : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "y"                 : (widgets.Dropdown,             {"options":col_list                                                                   }),
        "y_jitter"          : (widgets.FloatText,            {"value":.1                                                                           }),
        "y_partial"         : (widgets.Dropdown,             {"options":col_list                                                                   }),
    }

    def __call__(self, arg_name, descrp=True):
        widget, kwargs = self.widget_map[arg_name]
        if descrp != "Column selector":
            kwargs["description"]=arg_name
        return widget(**kwargs)

import collections
SEABORN_PLOTS ={
    "relplot":{
            "x"       : "x",
            "y"       : "y",
            "hue"     : "hue",
            "size"    : "size_vector",
            "style"   : "style",
            "row"     : "row",
            "col"     : "col",
            "col_wrap": "col_wrap",
            #"row_order":
            #"col_order":
            "palette" : "palette",
            #"hue_order":
            #"hue_norm":
            #"sizes"
            #"size_order":
            #"size_norm":
            "legend"  : "legend",
            "kind"    : "kind_relplot",
            "height"  : "height",
            "aspect"  : "aspect",
        },
        "scatterplot":{
            "x": "x",
            "y": "y",
            "hue": "hue",
            "size": "size_vector",
            "style": "style",
            "palette": "palette",
            #"hue_order":
            #"hue_norm":
            #"sizes": "sizes",
            #"size_order":
            #"size_norm":
            #"markers":
            #"style_order":
            #"{x,y}_bins": (non functional)
            #"units": (non functional)
            #"estimator": (non functional)
            #"ci": (non functional)
            #"n_boot": (non functional)
            "alpha": "alpha",
            #"{x,y}_jitter": (non functional)
            "legend": "legend",
        },
    "lineplot":{
            "x": "x",
            "y": "y",
            "hue": "hue",
            "size": "size_vector",
            "style": "style",
            "palette": "palette",
            #"hue_order":
            #"hue_norm":
            #"sizes",
            #"dashes":,
            #"markers"
            #"style_order":
            "units": "units",
            #"estimator"
            "ci": "ci",
            "n_boot": "n_boot",
            "sort": "sort",
            "err_style": "err_style",
            "legend": "legend",
        },"catplot":{
            "x": "x",
            "y": "y",
            "row": "row",
            "col": "col",
            "col_wrap": "col_wrap",
            #"estimator"
            "ci": "ci",
            "n_boot": "n_boot",
            "units": "units",
            #"order","hue_order"
            #"row_order","col_order"
            "kind": "kind_catplot",
            "height": "height",
            "aspect": "aspect",
            "orient": "orient",
            "color": "color",
            "palette": "palette",
            "legend": "legend",
            "legend_out": "legend_out",
            "sharex": "sharex",
            "sharey": "sharey",
            "margin_titles": "margin_titles",
        },"stripplot":{
            "x": "x",
            "y": "y",
            #"order","hue_order"
            "jitter": "jitter",
            #"dodge"
            "orient": "orient",
            "color": "color",
            "palette": "palette",
            "size": "size_float",
            "edgecolor": "edgecolor",
            "linewidth": "linewidth",
        },"swarmplot":{
            "x": "x",
            "y": "y",
            #"order","hue_order"
            #"dodge"
            "orient": "orient",
            "color": "color",
            "palette": "palette",
            "size": "size_float",
            "edgecolor": "edgecolor",
            "linewidth": "linewidth",
        },"boxplot":{
            "x": "x",
            "y": "y",
            #"order","hue_order"
            "orient": "orient",
            "color": "color",
            "palette": "palette",
            "saturation": "saturation",
            "width": "width",
            #"dodge"
            "fliersize": "fliersize",
            "linewidth": "linewidth",
            "whis":  "whis",
            "notch": "notch",
        },"violinplot":{
            "x": "x",
            "y": "y",
            "hue": "hue",
            #"order","hue_order"
            "bw": "bw",
            "cut": "cut",
            "scale": "scale_violinplot",
            "scale_hue": "scale_hue",
            "gridsize": "gridsize",
            "width": "width",
            "inner": "inner",
            "split": "split",
            #"dodge"
            "orient": "orient",
            "linewidth": "linewidth",
            "color": "color",
            "palette": "palette",
            "saturation": "saturation",
        },"boxenplot":{
            "x": "x",
            "y": "y",
            "hue": "hue",
            #"order","hue_order"
            "orient": "orient",
            "color": "color",
            "palette": "palette",
            "saturation": "saturation",
            "width": "width",
            #"dodge"
            "k_depth": "k_depth",
            "linewidth": "linewidth",
            "scale":  "scale_boxenplot",
            "outlier_prop": "outlier_prop",
        },"pointplot":{
        "x": "x",
        "y": "y",
        "hue": "hue",
        #"order","hue_order"
        #"estimator"
        "ci": "ci",
        "n_boot": "n_boot",
        "units": "units",
        #"markers"
        #linestyles
        #"dodge"
        "join": "join",
        "scale": "scale_float",
        "orient": "orient",
        "color": "color",
        "palette": "palette",
        "errwidth": "errwidth",
        "capsize": "capsize",
    },"barplot":{
        "x": "x",
        "y": "y",
        "hue": "hue",
        #"order","hue_order"
        #"estimator"
        "ci": "ci",
        "n_boot": "n_boot",
        "units": "units",
        "orient": "orient",
        "color": "color",
        "palette": "palette",
        "saturation": "saturation",
        #"errcolor"
        "errwidth": "errwidth",
        "capsize": "capsize",
        #"dodge"
    },"countplot":{
        "x": "x",
        "y": "y",
        "hue": "hue",
        #"order","hue_order"
        "orient": "orient",
        "color": "color",
        "palette": "palette",
        "saturation": "saturation",
        #"dodge"
    },"jointplot":{
        "x": "x",
        "y": "y",
        "kind": "kind_jointplot",
        #stat_func
        "color": "color",
        "height": "height",
        "ratio": "ratio",
        "space": "space",
        "dropna": "dropna",
        #"xlim"
        #"ylim"
    },"pairplot":{
        "hue": "hue",
        #hue_order
        "palette": "palette",
        #vars
        #x_vars
        #y_vars
        "kind": "kind_pairplot",
        "diag_kind": "diag_kind",
        #"markers"
        "height": "height",
        "aspect": "aspect",
        "dropna": "dropna",
    },"displot":{
        "a": "a",
        "bins": "bins",
        "hist": "hist",
        "kde": "kde",
        "rug": "rug",
        #"fit"
        #{hist, kde, rug, fit}_kws
        "color": "color",
        "vertical": "vertical",
        "norm_hist": "norm_hist",
        "axlabel": "axlabel",
        "label": "label",
    },"kdeplot":{
        "data": "data",
        "data2": "data2",
        #"x":"x",
        #"y":"y",
        "shade": "shade",
        "vertical": "vertical",
        #removed("kernel": "kernel",)
        "bw": "bw",
        "gridsize": "gridsize",
        "cut": "cut",
        #"clip":
        "legend": "legend",
        "cumulative": "cumulative",
        "shade_lowest": "shade_lowest",
        "cbar": "cbar",
        "cbar_ax": "cbar_ax",
    },"lmplot":{
        "x": "x",
        "y": "y",
        "hue": "hue",
        "col": "col",
        "row": "row",
        "palette": "palette",
        "col_wrap": "col_wrap",
        "height": "height",
        "aspect": "aspect",
        #"markers",
        "sharex": "sharex",
        "sharey": "sharey",
        "legend": "legend",
        "legend_out": "legend_out",
        #x_estimator
        "x_bins": "x_bins",
        "x_ci": "x_ci",
        "scatter": "scatter",
        "fit_reg": "fit_reg",
        "ci": "ci",
        "n_boot": "n_boot",
        "units": "units",
        "order": "order_regression",
        "logistic": "logistic",
        "lowess": "lowess",
        "robust": "robust",
        "logx": "logx",
        "x_partial": "x_partial",
        "y_partial": "y_partial",
        "truncate": "truncate",
        "x_jitter": "x_jitter",
        "y_jitter": "y_jitter",
    },"regplot":{
        "x": "x",
        "y": "y",
        #x_estimator
        "x_bins": "x_bins",
        "x_ci": "x_ci",
        "scatter": "scatter",
        "fit_reg": "fit_reg",
        "ci": "ci",
        "n_boot": "n_boot",
        "units": "units",
        "order": "order_regression",
        "logistic": "logistic",
        "lowess": "lowess",
        "robust": "robust",
        "logx": "logx",
        "x_partial": "x_partial",
        "y_partial": "y_partial",
        "truncate": "truncate",
        "x_jitter": "x_jitter",
        "y_jitter": "y_jitter",
        "label": "label",
        "color": "color",
        "marker": "marker",
    },"residplot":{
        "x": "x",
        "y": "y",
        "lowess": "lowess",
        "x_partial": "x_partial",
        "y_partial": "y_partial",
        "order": "order_regression",
        "robust": "robust",
        "dropna": "dropna",
        "label": "label",
        "color": "color",
    },"heatmap":{
        "vmin": "vmin",
        "vmax": "vmax",
        "cmap": "cmap",
        "center": "center",
        "robust": "robust",
        "annot": "annot",
        "fmt": "fmt",
        "linewidths": "linewidths",
        "linecolor": "linecolor",
        "cbar": "cbar",
        "square": "square",
        #xticklabels, yticklabels
        #"mask"
    },"histplot":{
        "x":"x",
        "y":"y",
        "hue":"hue",
        #"weights":"weights", 
        #"stat":"stat", 
        "bins":"bins", 
        #"binwidth": "binwidth", 
        #"binrange": "binrange", 
        #"discrete": "discrete", 
        "cumulative": "cumulative", 
        #"common_bins": "common_bins",
        #"common_norm": "common_norm", 
        #"multiple": "multiple", 
        #"element": "element", 
        #"fill": "fill", 
        #"shrink": "shrink", 
        "kde": "kde",
        #"kde_kws": "kde_kws", 
        #"line_kws": "line_kws", 
        #"thresh": "thresh", 
        #"pthresh": "pthresh",
        #"pmax": "pmax",
        "cbar": "cbar",
        "cbar_ax": "cbar_ax",
        #"cbar_kws": "cbar_kws", 
        "palette": "palette", 
        #"hue_order": "hue_order",
        #"hue_norm": "hue_norm", 
        "color": "color",
        #"log_scale": "log_scale",
        "legend": "legend", 
        #"ax": "None", 
        #"**kwargs)
    }
}
    
SEABORN_PLOTS = collections.OrderedDict(sorted(SEABORN_PLOTS.items()))


    

def seaborn_plot(df, plot_type, kwargs):
    method = getattr(seaborn, plot_type)
    if plot_type not in ["distplot", "kdeplot"]:
        kwargs["data"]=df
    return method(**kwargs)
