from unsupervised_clustering_deprec import DBSCAN
from sklearn.datasets import make_moons
X, _ = make_moons(250)

def time() :
    import time
    start_time = time.time()
    dbscan = DBSCAN()
    dbscan.fit_predict(X, eps = 0.45, min_neighbors = 20)
    return time.time() - start_time

python =time()

from cython_unsupervised_clustering import DBSCAN
cython = time()

print("py : ", python, " cython : ", cython)

#RO vs. RC