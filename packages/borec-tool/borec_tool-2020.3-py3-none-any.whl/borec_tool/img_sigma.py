from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThreadPool
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import traceback, sys
import scipy.stats as st
from skimage.restoration import estimate_sigma


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


class Sigma(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4):
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.threadpool = QThreadPool()
        self.show()

    def draw_fig(self, mean_ci):
        x = range(len(mean_ci[0]))
        self.axes.plot(x, mean_ci[0])
        self.axes.fill_between(x, mean_ci[1], mean_ci[2], alpha=.3)
        self.axes.figure.canvas.draw()
        self.show()

    def process(self, input):
        shape = input.data.shape
        img = input.data
        bands = input.header.bands.centers
        est_sigma = estimate_sigma(img, average_sigmas=False, multichannel=True)
        self.axes.plot(bands, est_sigma)

        self.axes.set(xlabel='wavelength [nm]', ylabel = '$\hat{\sigma}$')
        self.axes.figure.canvas.draw()
        self.show()

        # ax2 = sns.swarmplot(data=self.df_data, color=".25")
#        ax2.plot()
