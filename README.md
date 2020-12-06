# iseaborn

A simple wrapper around `seaborn` using `ipwidygets` for interactive plots in Jupyterlab.

Can be used in 2 ways :
 - discover the seaborn package, its plots possibilities, and the effect of the different parameters
 - quick-simple Exploratory Data Analysis (EDA) on pandas' DataFrame

# Example

```python
%matplotlib ipympl
import seaborn as sns

iris = sns.load_dataset("iris")

from iseaborn import heatmap

heatmap(iris)
```

Or more visually : 

![examples.gif](examples.gif)

# TODO/IDEAS
 - [ ] : add a title on plots based on plot type ?
 - [ ] : add a title based on df name ?
 - [ ] : clean palettes list
 - [ ] : add support for `sns.set_style`
 - [ ] : add support for `sns.set_context`
 - [ ] : add support for `sns.set_palette()`
 - [ ] : use tight_layout ?
 - [ ] : add a FacetGrid/Grid wrapper ?
 
# See also

https://github.com/chmduquesne/quickviz
https://github.com/pseudoPixels/iSeaborn
https://github.com/TrainingByPackt/Interactive-Data-Visualization-with-Python
https://gist.github.com/noklam/ddd503085c5aa0c27ddb0eceb4a2f07b


