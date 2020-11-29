# iseaborn

A simple wrapper around `seaborn` using `ipwidygets` for interactive plots in Jupyterlab.

# Example

```python
%matplotlib ipympl
import seaborn as sns

iris = sns.load_dataset("iris")

from iseaborn import heatmap

heatmap(iris)
```