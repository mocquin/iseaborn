
# retirer les warning de plots 
Soit avec 
```python
import warnings
warnings.filterwarnings("ignore")
```

soit en fermant les figures explicitements : https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot-in-matplotlib
```python
plt.close(fig)
```