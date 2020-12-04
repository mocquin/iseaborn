
 
import matplotlib
import pandas as pd
import ipywidgets as widgets
from . import pandas
from . import seaborn
from IPython.display import display, clear_output
from ipywidgets.widgets.interaction import show_inline_matplotlib_plots




class UI(object):
    def __init__(self, df, gen_widgets, plot):
        # storing the dataframe
        self.df = df
        # init a dict of "manual kwargs"
        self.manual_kwargs = {}
        # call the "gen_widgets" function on the dataframe to create the widgets
        self.widgets = gen_widgets(df)
        # store the plot function
        self.plot = plot
        # init a list of connected args
        self.connected_args = []
        # connect all widgets's values to observe the "self.display_plot" to trigger a replot on any widget change
        self.connect_widgets()
 

        #### WIDGETS : use self.get_plot_types() / self.redraw() / self.add_arg
        # HBox avec liste dropdown des plot disponibles, et checkbox pour autoupdate
        # create a plot_type HBox widget
        self.plot_type_box = widgets.HBox()
        # create a plot_type chooser using Dropdown widget, options being from self.get_plot_types()
        self.plot_type_chooser = widgets.Dropdown(options=self.get_plot_types(), description='Plot type')
        # create a auto_update checkbox widget
        self.auto_update = widgets.Checkbox(description='auto-update')
        # add the plot_type chooser Dropdown and the auto_update checkbox
        self.plot_type_box.children = [self.plot_type_chooser, self.auto_update]
        # observe the plot choice and redraw
        self.plot_type_chooser.observe(self.redraw, 'value')
        # observe the autoupdate and redraw
        self.auto_update.observe(self.redraw, 'value')
 
        # HBox avec liste dropdown des args à ajouter
        # create a HBox widget
        self.add_arg_box = widgets.HBox()
        # create a Dropdown widget for "add arg"
        self.arg_chooser = widgets.Dropdown(description='Add arg')
        # add the Dropdown chooser widget to the HBox
        self.add_arg_box.children = [self.arg_chooser]
        # add observer to the Dropdown value with self.add_arg method
        self.arg_chooser.observe(self.add_arg, 'value')
 
        # create a VBox and Output widgets
        self.vbox = widgets.VBox()
        self.output = widgets.Output()

        # Display the VBox and Output
        display(self.vbox, self.output)

        ## REDRAW
        # redraw : most of the work is done there
        self.redraw()

    def connect_widgets(self):
        """
        Make sure that a change to any of the widgets triggers a replot
        """
        # récupère tous les widgets, et observe leurs valeurs avec display_plot
        for w in self.widgets['*'].values():
            w.observe(self.display_plot, 'value')

    def get_plot_types(self):
        """
        All the plot types
        """
        # pour créer la liste des plots possibles, utilisé à l'init dans le dropdown du plot chooser
        # récupère la liste des noms du dict "*" dans le dict self.widget, qui contient un dict par type de plot, avec comme clé le nom du plot
        # self.widget est un dict renvoyé par la fonction "gen_widget" passée à l'init (externe au module)
        return sorted([p for p in self.widgets.keys() if p != '*'])

    def get_accepted_args(self):
        """
        Arguments that are accepted by the currently selected plot type
        """
        # récupère le type de plot courant
        p = self.plot_type_chooser.value
        # récupère la liste des noms des args possibles pour ce type de plot
        args = sorted(self.widgets[p].keys())
        # place the most useful arguments on top
        top = ['x', 'y']
        for t in reversed(top):
            if t in args:
                args.remove(t)
                args = [t] + args
        # renvoi la liste des noms des args possibles pour le plot en cours
        return args
 
    def add_arg(self, *_):
        """
        Add the argument selected by the user in the plot arguments
        """
        # si l'arg sélectionné en cour n'est pas déjà dans connected_args
        if self.arg_chooser.value not in self.connected_args:
            # on l'ajoute
            self.connected_args.append(self.arg_chooser.value)
            self.redraw()
 
    def get_widget(self, arg):
        """
        Return the widget associated with the argument. Which widget is
        returned for a given argument name depends on the selected plot
        type.
        """
        # récupère le type de plot
        p = self.plot_type_chooser.value
        # récupère le widget associé au couple (type de plot / nom de l'arg)
        return self.widgets[p][arg]
 
    def gen_arg_line(self, arg):
        """
        Create a line, ready to be inserted, containing the widget
        associated with  the argument, as well as a remove button. The
        remove button should not only remove the line, but also remove the
        argument from the connected arguments.
        """
        w = self.get_widget(arg)   # récupère le widget associé au couple (type de plot / nom de l'arg)
        w.description = arg
        r = widgets.Button(description='remove')
        h = widgets.HBox(children=[w, r])
        def remove(*_):
            for c in h.children:
                if c != w:
                    c.close()
            h.close()
            self.connected_args.remove(arg)
            self.redraw()
        r.on_click(remove)
        return h
 
    def filter_connected_args(self):
        """
        Remove from the connected arguments any argument that is
        irrelevant for the current plot type
        """
        # update self.connected_args list content, by only keeping
        # the args that are accepted
        # connected_args est une liste de noms d'args
        # liste des args possibles pour le plot en cours : get_accepted_args
        self.connected_args = [
            a for a in self.connected_args[:]
            if a in self.get_accepted_args()
        ]
 
    def save(self):
        """
        Save the UI state in a dictionary
        """
        return {
            'plot': self.plot_type_chooser.value,
            'kwargs': self.kwargs(),
        }
 
    def load(self, d):
        """
        Load a dictionary into the UI state
        """
        for k in d.keys():
            if k not in ['plot', 'kwargs']:
                raise ValueError('%s: unexpected key')
        plot = d['plot']
        if plot not in self.get_plot_types():
            raise ValueError('%s: not an acceptable plot type' % plot)
        self.plot_type_chooser.value = plot
        for arg in d['kwargs'].keys():
            if arg not in self.get_accepted_args():
                raise ValueError('%s: not an acceptable arg' % arg)
        self.connected_args = list(d['kwargs'].keys())
        self.redraw()
        for arg, value in d['kwargs'].items():
            self.get_widget(arg).value = value
        self.auto_update.value = True
 
    def kwargs(self):
        """
        Return a kwarg dictionary associated with the current UI state
        """
        # récupère le widget associé au couple (type de plot en cours et nom de l'arg, pour tous les args dans connected args)
        # et associe le nom de l'arg avec la valeur du widget correspondant
        # connected args est une liste de noms de param valide pour le plot en cours
        return {
            arg:self.get_widget(arg).value for arg in self.connected_args
        }
 
    def gen_plot(self):
        """
        Return the plot object associated with the UI state
        """
        # récupère les kwargs : les kwargs associés aux widgets définis dans connected_args : liste vide créée à l'init
        kwargs = self.kwargs()
        # ajoute les manual_kwargs : dictionnaire vide créé à l'init
        kwargs.update(**self.manual_kwargs)
        # récupère le type de plot via la valeur du widget
        plot_type = self.plot_type_chooser.value
        # utilise la fonction plot enregistrée à l'init, sur le df, avec le type de plot, et les kwargs
        return self.plot(self.df, plot_type, kwargs)
 
    def display_plot(self, *_):
        """
        Display the plot object associated with the UI state, unless the
        user does not want interactive updates
        """
        # si l'auto upadte est désactivé, ne fait rien
        if not self.auto_update.value:
            return
        show_inline_matplotlib_plots()
        # sinon, clear l'output
        with self.output:
            # clear_output de IPython.display
            clear_output(wait=True)
            self.gen_plot()
            show_inline_matplotlib_plots()
 
    def redraw(self, *_):
        """
        Redraw all the UI buttons so that they match the internally
        selected args, then display the plot
        """
        # remove the args from the connected_args list 
        # that are not valid for the current plot type
        self.filter_connected_args()
 
        # récupère la plot_type_box qui contient le dropdown des plots et le checkbox d'autoupdate
        lines = []
        lines.append(self.plot_type_box)
        # pour tous les args connected
        for arg in self.connected_args:
            # créé une ligne HBox
            lines.append(self.gen_arg_line(arg))
        # ligne de séparation des inputs
        lines.append(widgets.HBox([widgets.Label(value='---')]))
        # ajoute le dropdown d'ajout de arg
        lines.append(self.add_arg_box)
        self.vbox.children = lines
 
        # récupère le nom de l'arg à ajouter en cours
        arg_choice = self.arg_chooser.value
        # avoid accidentally adding args during redraw
        self.arg_chooser.unobserve(self.add_arg, 'value')
        self.arg_chooser.options = self.get_accepted_args()
        # restore choice if possible
        if arg_choice in self.get_accepted_args():
            self.arg_chooser.value = arg_choice
        else:
            self.arg_chooser.value = None
        self.arg_chooser.observe(self.add_arg, 'value')
 
        # display final 
        self.display_plot()
 
    def __add__(self, other):
        """
        Overlays self and other. Probably buggy.
        """
        if not isinstance(other, UI):
            raise TypeError("wrong type for %s" % str(other))
        p = self.gen_plot()
        if not isinstance(p, matplotlib.axes.Axes):
            p = p.ax
        restore = ("ax" in other.manual_kwargs)
        old_ax = other.manual_kwargs.get("ax")
        other.manual_kwargs["ax"] = p
        other.gen_plot()
        if restore:
            other.manual_kwargs["ax"] = old_ax
        else:
            del other.manual_kwargs["ax"]
        return other
 

def visualize_pandas(df):
    return UI(
            df,
            gen_widgets=pandas.gen_widgets,
            plot=pandas.plot
            )
 

def visualize_seaborn(df):
    return UI(
            df,
            gen_widgets=seaborn.gen_widgets,
            plot=seaborn.plot
            )
 

# main function, returns a UI instance with corresponding widgets and plot functions
def visualize(df, method='seaborn'):
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError('The argument must be a pandas dataframes')
    if method == 'pandas':
        return visualize_pandas(df)
    elif method == 'seaborn':
        return visualize_seaborn(df)
    else:
        raise ValueError('unsupported method')