import ipywidgets as widgets
#import seaborn
import pandas as pd




class PandasWidgetDispenser(object):
    """
    Example
    -------

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
            "a_select"          : (widgets.SelectMultiple, {"options":col_list, "description":"Column selector"         }),
            "a_select_ext"      : (widgets.SelectMultiple, {"options":col_list_ext                                      }),
            "C"                 : (widgets.Dropdown      , {"options":col_list                                          }),
            "bins"              : (widgets.IntText       , {"value":10                                                  }),
            "bw_method"         : (widgets.Dropdown      , {"options":["scott", "silverman"]                            }),
            "by"                : (widgets.Dropdown      , {"options":col_list                                          }),
            "c"                 : (widgets.Dropdown      , {"options":col_list                                          }),
            "colormap"          : (widgets.Text          , {                                                            }),
            "column"            : (widgets.SelectMultiple, {"tiple(options":col_list                                    }),
            "fontsize"          : (widgets.IntSlider     , {"(min":2, "max":40                                          }),
            "grid"              : (widgets.Checkbox      , {                                                            }),
            "gridsize"          : (widgets.IntText       , {"value":100                                                 }),
            "ind"               : (widgets.IntText       , {"value":1000                                                }),
            "legend"            : (widgets.Checkbox      , {                                                            }),
            "logx"              : (widgets.Checkbox      , {                                                            }),
            "logy"              : (widgets.Checkbox      , {                                                            }),
            "mark_right"        : (widgets.Checkbox      , {                                                            }),
            "position"          : (widgets.FloatSlider   , {"min":0.0, "max":1.0, "step":0.05                           }),
            "s"                 : (widgets.Dropdown      , {"options":dict([(col, list(df[col])) for col in list(df)])  }),
            "sharex"            : (widgets.Checkbox      , {                                                            }),
            "sharey"            : (widgets.Checkbox      , {                                                            }),
            "sort_columns"      : (widgets.Checkbox      , {                                                            }),
            "stacked"           : (widgets.Checkbox      , {                                                            }),
            "subplots"          : (widgets.Checkbox      , {                                                            }),
            "title"             : (widgets.Text          , {                                                            }),
            "use_index"         : (widgets.Checkbox      , {                                                            }),
            "x"                 : (widgets.Dropdown      , {"options":col_list                                          }),
            "xerr"              : (widgets.Dropdown      , {"options":dict([(col, list(df[col])) for col in list(df)])  }),
            "y"                 : (widgets.Dropdown      , {"options":col_list                                          }),
            "yerr"              : (widgets.Dropdown      , {"options":dict([(col, list(df[col])) for col in list(df)])  }),
        }

    def __call__(self, arg_name, descrp=True):
        widget, kwargs = self.widget_map[arg_name]
        if descrp != "Column selector":
            kwargs["description"]=arg_name
        return widget(**kwargs)


    
    
import collections

_PLOTS = {
    "area": {},
    "bar": {},
    "barh": {},
    "box": {
        "by": "by",
    },
    "density": {
        "bw_method": "bw_method",
        "ind": "ind",
    },
    "hexbin": {
        "C": "C",
        "gridsize": "gridsize",
    },
    "hist": {
        "by": "by",
        "bins": "bins",
    },
    "kde": {
        "bw_method": "bw_method",
        "ind": "ind",
    },
    "line": {},
    "pie": {},
    "scatter": {
        "s": "s",
        "c": "c",
    },
    "boxplot": {
        "by": "by",
    },
    "hist": {
        "by": "by",
        "bins": "bins",
        "column": "column",
    }
}

generic_args = {
        k:k for k in [ "x", "y", "subplots", "sharex", "sharey",
            "use_index", "title", "grid", "legend", "logx", "logy",
            "fontsize", "colormap", "position", "xerr", "yerr",
            "stacked", "sort_columns", "mark_right", ]
}

for plot_type, plot_dict in _PLOTS.items():
    _PLOTS[plot_type].update(**generic_args)



PANDAS_PLOTS = collections.OrderedDict(sorted(_PLOTS.items()))




def plot(df, plot_type, kwargs):
    method = getattr(df.plot, plot_type)
    #if plot_type not in ["distplot", "kdeplot"]:
    #    kwargs["data"]=df
    return method(**kwargs)
