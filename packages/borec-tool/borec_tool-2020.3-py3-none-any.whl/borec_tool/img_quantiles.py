from PyQt5 import QtWidgets
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThreadPool
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import traceback, sys
from .data_utilities import statistics


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


class Quantiles(FigureCanvas):

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
        self.axes.clear()
        self.axes.plot(x, mean_ci[0])
        self.axes.fill_between(x, mean_ci[1], mean_ci[2], alpha=.3)
        self.axes.figure.canvas.draw()
        self.show()

    def process(self, input):
        shape = input.data.shape
        img = input.data
        bands = input.header.bands.centers
        self.dict_data = statistics.quantiles(img)
        self.axes.clear()
        q1 = self.dict_data['quantile-0']
        q2 = self.dict_data['quantile-1']
        q3 = self.dict_data['quantile-2']
        self.axes.plot(bands, q2, label='median')
        self.axes.fill_between(bands, q1, q3, alpha=0.2, label='q25-q75')
        self.axes.legend()
        self.axes.set(xlabel='Wavelength [nm]', ylabel = 'Intensity')
        self.axes.figure.canvas.draw()
        self.show()
