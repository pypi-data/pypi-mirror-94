from hdbscan import HDBSCAN
from sklearn.decomposition import PCA
import numpy as np

class PCA_HDBSCAN():

    def __init__(self, n_components=None, min_cluster_size=1000):
        self.dbscan = HDBSCAN(min_cluster_size=min_cluster_size)
        self.pca = PCA(n_components)

    def fit(self, data):
        self.data = data
        self.shape = (-1,) + (data.shape[-1],)
        reduced_data = self.pca.fit_transform(data.reshape(self.shape))
        self.dbscan.fit(reduced_data)
        return self

    def predict(self, data):
        labels = self.dbscan.labels_
        return labels.reshape(data.shape[:2])

    @property
    def cluster_centers_(self):
        labels = self.dbscan.labels_
        n_clusters = labels.max()+1
        data_ravel = self.data.reshape(self.shape)
        centers = np.squeeze(np.array([np.mean(data_ravel[np.nonzero(labels==idx), :],1) for idx in range(n_clusters)]))
        return centers