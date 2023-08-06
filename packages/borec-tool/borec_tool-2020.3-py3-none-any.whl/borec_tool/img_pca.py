from PyQt5 import QtWidgets
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThreadPool
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import traceback, sys
from sklearn.decomposition import PCA


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


class EvalPCA(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4):
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)
        self.parameters = {'n_components': 200}
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.threadpool = QThreadPool()
        self.show()

    def pca_function(self, data, **kwargs):
        try:
            self.shape = (-1,) + (data.shape[-1],)
            self.pca = PCA(**kwargs)
            self.pca.fit(data.reshape(self.shape))
            return self.pca
        except ValueError:
            return None



    def process(self, input=None):
        if input is not None: self.data = input
        shape = input.data.shape
        self.bands = input.header.bands.centers
        worker = Worker(self.pca_function, self.data.data, **self.parameters)
        worker.signals.result.connect(self.show_output)
        self.threadpool.start(worker)

    def show_output(self, output):
        ev = output.explained_variance_ratio_
        self.axes.plot(np.cumsum(ev))
        self.axes.set(xlabel='Number of components', ylabel = 'Cumulative explained variance')
        self.axes.figure.canvas.draw()
        self.show()

