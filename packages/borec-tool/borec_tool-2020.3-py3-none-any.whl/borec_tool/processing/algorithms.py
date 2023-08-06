from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans, OPTICS

def k_means(data, init, n_clusters, max_iter, n_init=2):
    kmeans = KMeans(init=init, n_clusters=n_clusters, max_iter=max_iter, n_init=n_init)
    shape = (-1,)+(data.shape[-1],)
    estimator = make_pipeline(StandardScaler(), kmeans).fit(data.reshape(shape))
    labels = estimator.predict(data.reshape(shape))
    return labels.reshape(data.shape[:2])


class KMeans(KMeans):
    """KMeans++ hyperspectral"""

    def __init__(self, **kwargs):
        super(KMeans, self).__init__(**kwargs)

    def fit(self, data):
        self.shape = (-1,) + (data.shape[-1],)
        super(KMeans, self).fit(data.reshape(self.shape))
        return self

    def predict(self, data):
        labels = super(KMeans, self).predict(data.reshape(self.shape))
        return labels.reshape(data.shape[:2])

    def scaler_pipeline(self, *args):
        return make_pipeline(*args)

class MiniBatchKMeans(MiniBatchKMeans):
    """KMeans++ hyperspectral"""

    def __init__(self, **kwargs):
        super(MiniBatchKMeans, self).__init__(**kwargs)

    def fit(self, data):
        self.shape = (-1,) + (data.shape[-1],)
        super(MiniBatchKMeans, self).fit(data.reshape(self.shape))
        return self

    def predict(self, data):
        labels = super(MiniBatchKMeans, self).predict(data.reshape(self.shape))
        return labels.reshape(data.shape[:2])

    def scaler_pipeline(self, *args):
        return make_pipeline(*args)

