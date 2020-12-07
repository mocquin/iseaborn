import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as ipyw
import pandas as pd

from IPython.display import display, clear_output
from ipywidgets.widgets.interaction import show_inline_matplotlib_plots

from seaborn_widgets_map import SeabornWidgetDispenser, SEABORN_PLOTS
from pandas_widgets_map import PandasWidgetDispenser, PANDAS_PLOTS



class PlotUI(ipyw.HBox):
    
    def __init__(self, df, plot_name, interface="seaborn", figsize=(6.4, 4.8)):
        if not isinstance(df, pd.DataFrame):
            raise ValueError
        super().__init__()
        self.figsize = figsize
        self.df = df
        self.plot_name = plot_name
        
        # set plot dict
        if interface=="seaborn":
            PLOTS = SEABORN_PLOTS
            WidgetDispenser = SeabornWidgetDispenser
            self.module = sns
        elif interface == "pandas":
            PLOTS = PANDAS_PLOTS
            WidgetDispenser = PandasWidgetDispenser
            self.module = df.plot
        else:
            raise ValueError("Wrong interface")
        self.interface = interface
    
        plot_dict = PLOTS[plot_name]
        wdispenser = WidgetDispenser(df)
        
        self.widgets_names = []
        self.widgets_list  = []
        self.wdict = {}

        # create a VBox and Output widgets
        vbox = ipyw.VBox()
        hbox = ipyw.HBox()
        self.output = ipyw.Output()

        # columns selector
        self.cols_selector = wdispenser("a_select")
        self.cols_selector.value = [f for f in self.df]
        
        # create widgets and add them to the HBox
        for arg_name, widget_name in plot_dict.items():
            # create widget
            w = wdispenser(widget_name, descrp=False)
            
            self.widgets_names.append(arg_name)
            cb = self._create_enable_checkbox(descr=arg_name)
            self._link_enable_status(w, cb)
            self.wdict[arg_name] = (cb, w)
            
            box = [cb, w]
            
            self.widgets_list.append(ipyw.HBox(box))
        
        self._set_init_values_widgets()
        
        self.connect_widgets()
        
        # set the widgets in a VBox
        vbox.children = [self.cols_selector] + [*self.widgets_list]
        
        # wrap all the UI for the plot in a hbox
        self.children = [vbox, self.output]
        
        # initial plot call
        with self.output:
            fig, ax = plt.subplots(figsize=self.figsize)
            self.fig = fig
        self.display_plot()
    

    def _set_init_values_widgets(self):
        """Init some args for specific plot types"""
        if self.interface == "seaborn":
            if self.plot_name in ["regplot", "residplot", "lmplot"]:
                self.wdict["x"][0].value = False
                self.wdict["y"][0].value = False
            elif self.plot_name in ["kdeplot"]:
                self.wdict["data"][0].value = False    
                
        elif self.interface == "pandas":
            if self.plot_name in ["hexbin", "scatter"]:
                self.wdict["x"][0].value = False
                self.wdict["y"][0].value = False
            elif self.plot_name in ["pie"]:
                self.wdict["y"][0].value = False
        
        
    def _create_enable_checkbox(self, descr="Disable:"):
        """Create a checkbox"""
        return ipyw.Checkbox(description=descr, value=True, indent=False, layout=ipyw.Layout(width="300px"))
    
    
    def _link_enable_status(self, w, cb):
        """Link checkbox values to widget disabled value"""
        return ipyw.link((cb, "value"), (w, "disabled"))


    def connect_widgets(self):
        """Observe widgets values and checbox to trigger a replot"""
        for wbox in self.widgets_list:
            children = wbox.children
            children[1].observe(self.display_plot, 'value')    
            children[0].observe(self.display_plot, "value")
        # change in sub cols
        self.cols_selector.observe(self.display_plot, "value")
            
            
    def retrieve_enabled_kwargs(self):
        """Retrieve values of args that are enabled into a dict"""
        kwargs = {}
        for wbox, wname in zip(self.widgets_list, self.widgets_names):
            children = wbox.children
            if children[0].value == False:
                kwargs[wname] = children[1].value   
        return kwargs
    
        
    def display_plot(self, *_):
        # clear_output de IPython.display
        plt.close(self.fig)
        show_inline_matplotlib_plots()   
        with self.output:
            clear_output(wait=True)
            kwargs = self.retrieve_enabled_kwargs()
            # get all widgets names and values in a dict
            
            self.plot(kwargs)
            show_inline_matplotlib_plots()   
            
            
    def plot(self, kwargs):
        # select sub cols
        sub_df = self.df[list(self.cols_selector.value)]
        # get the plotting method from seaborn and plot with the kwargs
        method = getattr(self.module, self.plot_name)
        kwargs_str = self._format_kwargs(kwargs)
        display(f"{self.interface}.{self.plot_name}({kwargs_str})")
        # deal with specific plots

            
        if self.interface == "seaborn":
            if self.plot_name not in ["catplot", "relplot", "pairplot", "displot", "lmplot", "jointplot"]:
                fig, ax = plt.subplots(figsize=self.figsize)
                self.fig = fig
            if self.plot_name == "heatmap":
                kwargs["data"] = sub_df.corr()
            elif self.plot_name not in ["distplot", "kdeplot"]:
                kwargs["data"]= sub_df
            if self.plot_name not in ["catplot", "relplot", "pairplot", "displot", "lmplot", "jointplot"]:
                kwargs["ax"] = ax
        elif self.interface == "pandas":
            pass
        
        res = method(**kwargs)
        return res
    
    
    def _format_kwargs(self, kwargs):
        if not bool(kwargs):
            return ""
        def format_arg_on_type(arg):
            if isinstance(arg, str):
                return f"'{arg}'"
            return f"{arg}"
        return ", ".join([f"{t[0]}={format_arg_on_type(t[1])}" for t in kwargs.items()])
    

class BookletUI(ipyw.Tab):
    
    def __init__(self, df=None, plot_names=SEABORN_PLOTS.keys(), interface="seaborn", figsize=(6.4, 4.8)):
        super().__init__()
        
        if interface == "seaborn":
            plot_names = SEABORN_PLOTS.keys()
        elif interface == "pandas":
            plot_names = PANDAS_PLOTS.keys()
        else:
            raise ValueError("Wrong interface")
        
        self.df = df
        self.tab_names = []
        self.tab_contents = []
        
        for plot in plot_names:
            ui = PlotUI(self.df, plot, interface=interface, figsize=figsize)
            self.tab_names.append(plot)
            self.tab_contents.append(ui)
        
        self.children = self.tab_contents
        for i, name in enumerate(self.tab_names):
            self.set_title(i, name)
            
            