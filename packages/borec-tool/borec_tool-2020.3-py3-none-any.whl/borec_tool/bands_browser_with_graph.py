from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThreadPool, Qt
from PyQt5.QtWidgets import QWidget, QToolBar, QVBoxLayout, QHBoxLayout, \
    QLabel, QAction
from PyQt5.QtGui import QImage, QPixmap, QIcon
import seaborn as sns
import traceback, sys
import numpy as np
from numpy import ndarray
from pkg_resources import resource_filename

from .gui.param_box import StringBox, SpinBox
from .gui.parameters import StringBoxParams, SpinBoxParams
from .spectrum_window import SpectrumWindow
from borec_tool.gui.viewer import Viewer
from .gui.band_slider import Slider


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
            output = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(output)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class BandsBrowserWithGraph(QWidget):
    params = {}

    bands_sig = pyqtSignal(list)
    cube_sig = pyqtSignal(ndarray)

    def single_point_triggered(self, status):
        self.view.set_sel_mode(status)
        self.spectrum.set_clear(not status)

    def _set_val(self, key, idx):
        self.params[key] = self.parameters[key][idx]
        self.process()

    def __init__(self, parent=None, fun=None, wavelet=None, parameters=None):
        QWidget.__init__(self)
        self.fun = fun
        if parameters is not None:
            self.parameters = {}
            toolbar = QToolBar('Parameters')
            single_mark = QAction(QIcon(resource_filename('borec_tool.resources.gui', 'cursor-cross.png')), 'Mark', self)
            single_mark.triggered.connect(lambda state, status=False: self.single_point_triggered(status))
            toolbar.addAction(single_mark)
            multi_mark = QAction(QIcon(resource_filename('borec_tool.resources.gui', 'multi-cross.png')), 'Multiple marks', self)
            multi_mark.triggered.connect(lambda state, status=True: self.single_point_triggered(status))
            toolbar.addAction(multi_mark)
            toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.toolbar = toolbar
            for key, param in parameters.items():
                if isinstance(param, StringBoxParams):
                    self.parameters[key] = param.values
                    parambox = StringBox(param.values)
                    self.params[key] = parambox.currentText()
                    parambox.currentIndexChanged.connect(lambda idx, par_key=key:
                                                        self._set_val(par_key, idx))
                elif isinstance(param, SpinBoxParams):
                    self.parameters[key] = param.value
                    parambox = SpinBox(key, param)
                    parambox.valueChanged.connect(lambda value, par_key=parambox.key:
                                                  self._set_val(par_key, value))

                toolbar.addWidget(QLabel(param.label))
                toolbar.addWidget(parambox)
                spacer = QLabel()
                spacer.setFixedWidth(20)
                toolbar.addWidget(spacer)
        layout = QVBoxLayout()
        layout.addWidget(toolbar)

        self.spectrum = SpectrumWindow()
        self.bands_sig.connect(self.spectrum.set_bands)
        self.cube_sig.connect(self.spectrum.set_cube)

        img_layout = QHBoxLayout()

        view = Viewer(self)
        view.pos.connect(self.spectrum.draw_spectrum_at_pos)

        view.setMinimumHeight(512)
        self.view = view

        images = QWidget()
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(view)
        graph_layout.addWidget(self.spectrum)
        images.setLayout(graph_layout)
        self.images = images
        layout.addWidget(images)

        wavelet_slider = Slider(set_hidden=False)
        self.wavelet_slider = wavelet_slider
        wavelet_slider.band_idx.connect(self.set_band)
        layout.addWidget(wavelet_slider)

        self.setLayout(layout)
        self.threadpool = QThreadPool()

    def get_pixmap(self, band, output):
        image = output[:,:,band]
        image = np.uint8(image/np.float(np.max(output))*255)
        return QPixmap(QImage(image.tobytes(), *image.shape[0:2], image[0, :].nbytes, QImage.Format_Grayscale8))

    def set_data(self, data):
        self.data = data
        self.bands = data.header.bands.centers
        self.wavelet_slider.values = self.bands
        self.band = 0
        self.bands_sig.emit(self.bands)
        self.cube_sig.emit(self.data.data)

    def set_band(self, band):
        self.band = band
        self.display_raw()

    def set_output(self, output):
        self.output = output
        self.display_raw()

    def display_raw(self):
        if self.band is not None and self.output is not None:
            self.view.display_image(self.get_pixmap(self.band, self.output))

    def process(self, input=None):
        if input is not None:
            self.data = input
            self.set_data(self.data)
        worker = Worker(self.fun, self.data.data, **self.params)
        worker.signals.result.connect(self.set_output)
        self.threadpool.start(worker)
