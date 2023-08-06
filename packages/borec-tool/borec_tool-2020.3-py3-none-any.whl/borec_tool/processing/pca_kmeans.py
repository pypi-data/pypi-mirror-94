from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class PCA_KMeans():

    def __init__(self, n_components=None, n_clusters=None, init="k-means++", n_init=4, max_iter=100):
        self.kmeans = KMeans(n_clusters=n_clusters, init=init, n_init=n_init, max_iter=max_iter)
        self.pca = PCA(n_components)

    def fit(self, data):
        self.shape = (-1,) + (data.shape[-1],)
        reduced_data = self.pca.fit_transform(data.reshape(self.shape))
        self.kmeans.fit(reduced_data)
        return self

    def predict(self, data):
        reduced_data = self.pca.fit_transform(data.reshape(self.shape))
        labels = self.kmeans.predict(reduced_data)
        return labels.reshape(data.shape[:2])

    @property
    def cluster_centers_(self):
        centers = self.kmeans.cluster_centers_
        return self.pca.inverse_transform(centers)