import seaborn as sns
iris = sns.load_dataset("iris")

import ipywidgets as ipyw
import pivottablejs as pvt
from pivottablejs import pivot_ui
from IPython.display import HTML


def df_meta_ui(df):
    box = ipyw.HBox()
    out_left = ipyw.Output()
    out_right = ipyw.Output(layout=ipyw.Layout(width="100%"))
    desc_df = df.describe()
    box.children = [out_left, out_right]
    with out_left:
        df.info()
        display(desc_df)
        display(df.head())
    with out_right:
        display(pivot_ui(df))
    return box
 


ui = df_meta_ui(iris)

ui