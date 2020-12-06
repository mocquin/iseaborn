import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as ipyw
import pandas as pd

from IPython.display import display, clear_output
from ipywidgets.widgets.interaction import show_inline_matplotlib_plots

from seaborn_widgets_map import WidgetDispenser, PLOTS

hbox_layout = ipyw.Layout(width='800px')


class PlotUI(ipyw.HBox):
    
    def __init__(self, df, plot_name):
        if not isinstance(df, pd.DataFrame):
            raise ValueError
        super().__init__()
        self.df = df
        self.plot_name = plot_name
        
        # set plot dict
        self.plot_dict = PLOTS[plot_name]
        self.wdispenser = WidgetDispenser(df)
        
        self.enabled_args  = []
        self.widgets_names = []
        self.widgets_list  = []

        # create a VBox and Output widgets
        vbox = ipyw.VBox()
        hbox = ipyw.HBox()
        self.output = ipyw.Output()

        # columns selector
        self.cols_selector = self.wdispenser("a_select")
        self.cols_selector.value = [f for f in self.df]
        
        # create widgets and add them to the HBox
        for arg_name, widget_name in self.plot_dict.items():
            # create widget
            w = self.wdispenser(widget_name, descrp=False)
            
            self.widgets_names.append(arg_name)
            cb = self._create_enable_checkbox(descr=arg_name)
            self._link_enable_status(w, cb)
            
            box = [cb, w]
            
            self.widgets_list.append(ipyw.HBox(box))#, layout=hbox_layout))
        
        self.connect_widgets()
        
        # set the widgets in a VBox
        vbox.children = [self.cols_selector] + [*self.widgets_list]
        
        # wrap all the UI for the plot in a hbox
        self.children = [vbox, self.output]
        
        # initial plot call
        with self.output:
            fig, ax = plt.subplots()
            self.fig = fig
        self.display_plot()
    
    def _create_enable_checkbox(self, descr="Disable:"):
        return ipyw.Checkbox(description=descr, value=True, indent=False, layout=ipyw.Layout(width="300px"))
    
    def _link_enable_status(self, w, cb):
        return ipyw.link((cb, "value"), (w, "disabled"))


    def connect_widgets(self):
        for wbox in self.widgets_list:
            children = wbox.children
            children[1].observe(self.display_plot, 'value')    
            children[0].observe(self.display_plot, "value")
        self.cols_selector.observe(self.display_plot, "value")
            
    def retrieve_enabled_kwargs(self):
        kwargs = {}
        for wbox, wname in zip(self.widgets_list, self.widgets_names):
            children = wbox.children
            if children[0].value == False:
                kwargs[wname] = children[1].value   
        return kwargs
        
    def display_plot(self, *_):
        # clear_output de IPython.display
        clear_output(wait=True)
        #gen_plot()
        kwargs = self.retrieve_enabled_kwargs()
        # get all widgets names and values in a dict
        self.plot(kwargs)
        #show_inline_matplotlib_plots()   
            
    def plot(self, kwargs):
        plt.close(self.fig)
        sub_df = self.df[list(self.cols_selector.value)]
        with self.output:
            clear_output(wait=True)
            
            
            if self.plot_name not in ["catplot", "relplot", "pairplot", "displot", "lmplot", "jointplot"]:
                fig, ax = plt.subplots()
                self.fig = fig
            method = getattr(sns, self.plot_name)
            if self.plot_name == "heatmap":
                kwargs["data"] = sub_df.corr()
            elif self.plot_name not in ["distplot", "kdeplot"]:
                kwargs["data"]= sub_df
            if self.plot_name not in ["catplot", "relplot", "pairplot", "displot", "lmplot", "jointplot"]:
            # catplot is a figurelevel
                kwargs["ax"] = ax
                
            res = method(**kwargs)
            return res
    
    
# ajouter histplot
# regplot/residplot/lmplot : ajouter x/y par défaut
    

class SeabornBookletFull(ipyw.Tab):
    
    def __init__(self, df=None, plot_dict=PLOTS):
        super().__init__()
        
        self.df = df
        self.tab_names = []
        self.tab_contents = []
        
        for plot in plot_dict:
            ui = PlotUI(self.df, plot)
            self.tab_names.append(plot)
            self.tab_contents.append(ui)
        
        self.children = self.tab_contents
        for i, name in enumerate(self.tab_names):
            self.set_title(i, name)
            
            