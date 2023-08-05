from cython_python_testing import cython_tsne
tsne = cython_tsne.tSNE(1, 0.0014)
import numpy as np
from sklearn.datasets import make_blobs
X, _ = make_blobs(250)
x_transform = tsne.transform(X)

x_transform = [x_t.tolist() + [0] for x_t in x_transform]

import matplotlib.pyplot as plt
plt.cla()

def plot_points(points):
    import matplotlib.pyplot as plt
    plt.scatter([p[0] for p in points], [p[1] for p in points])

plot_points(x_transform)
plot_points(X)