from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QWidget, QToolBar, QVBoxLayout, QHBoxLayout, \
    QLabel
import seaborn as sns
import matplotlib.cm as cm
import numpy as np
import traceback, sys

from .gui.param_box import SpinBox
from .processing.algorithms import KMeans
from .gui.imshow_widget import ShowImage

from .spectrum_window import SpectrumWindow


def mean_ci_plot(data):
    g = sns.FacetGrid(data)
    g.map_dataframe(sns.relplot, x="variable", y="value", kind='line')
    return g.fig

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Clustering(QWidget):

    n_clust = 5
    n_iter = 100

    spectrum_sig = pyqtSignal(np.ndarray)

    def _set_val(self, key, value):
        self.parameters[key] = value
        self.process()

    def __init__(self, parent=None, parameters=None, clusterer=KMeans):
        QWidget.__init__(self)
        self.parameters = {}
        self.method = clusterer
        if parameters is not None:
            toolbar = QToolBar('Parameters')
            self.toolbar = toolbar
            for key, param in parameters.items():
                self.parameters[key] = param.value
                toolbar.addWidget(QLabel(param.label))
                parambox = SpinBox(key, param)
                parambox.valueChanged.connect(lambda value, par_key=parambox.key:
                                             self._set_val(par_key, value))
                toolbar.addWidget(parambox)

                spacer = QLabel()
                spacer.setFixedWidth(20)
                toolbar.addWidget(spacer)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        # widget with two image boxes side-by-side
        img_layout = QHBoxLayout()
        clusters = ShowImage(self)
        img_layout.addWidget(clusters)
        self.spectrum = SpectrumWindow()
        self.spectrum_sig.connect(self.spectrum.draw_vectors)
        img_layout.addWidget(self.spectrum)
        self.clusters = clusters
        imgbox = QWidget()
        imgbox.setLayout(img_layout)
        # add widget to layout
        layout.addWidget(imgbox)
        self.setLayout(layout)
        self.threadpool = QThreadPool()

    def clusterer_fn(self, data, function, **kwargs):
        try:
            self.clusterer = function(**kwargs).fit(data)
            return self.clusterer.predict(data)
        except ValueError:
            return None

    def show_output(self, output):
        if output is not None:
            self.output = output
            self.clusters.img_show(output, cmap=cm.Paired)
            self.spectrum_sig.emit(self.clusterer.cluster_centers_)

    def process(self, input=None):
        if input is not None: self.data = input
        parameters = self.parameters
        if not 'max_iter' in parameters or self.parameters['max_iter'] != 0:
            self.spectrum.set_bands(self.data.header.bands.centers)
            worker = Worker(self.clusterer_fn, self.data.data, self.method, **self.parameters)
            worker.signals.result.connect(self.show_output)
            self.threadpool.start(worker)

