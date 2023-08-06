from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import pyqtSignal
from .processing import process_bezier_svg
from dataclasses import dataclass
from pathlib import PurePosixPath
import numpy as np
from PyQt5 import QtWidgets
import scipy.io
from scipy.interpolate import interp1d
from pkg_resources import resource_filename

@dataclass
class Spectrum:
    x: []
    y: []
    min: int
    max: int
    status: bool

class LedSpectra(FigureCanvas):

    spectra = {}
    sig_switch = pyqtSignal(dict)

    def __init__(self, graphs, parent=None):
        fig = Figure(figsize=(4, 2))
        self.ax = fig.subplots()
        self.ax.set_visible(False)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.canvas = FigureCanvas()

        if graphs is not None:
            for name in graphs.keys():
                graph = graphs[name]
                self.spectra[name] = self.add_spectrum(graph)

    def add_spectrum(self, graph):
        graph_min = graph['x_scale'][0]
        graph_max = graph['x_scale'][1]
        x = range(graph_min, graph_max)
        if PurePosixPath(graph['path']).suffix == '.svg':
            toplot_f = process_bezier_svg.svg_to_function(graph['path'], graph['x_scale'],
                                                          graph['y_scale'])
            toplot = [(lambda x: toplot_f(v))(v) for v in x]
        elif PurePosixPath(graph['path']).suffix == '.mat':
            file = scipy.io.loadmat(resource_filename('borec_tool.resources',graph['path']))
            illum_Specim = interp1d(np.arange(graph_min,graph_max+10, 10), np.squeeze(file[list(file.keys())[-1]]))
            toplot_vect = illum_Specim(x)
            toplot = toplot_vect/np.max(toplot_vect)
        else:
            print('Throw exception!')
        return Spectrum(x, toplot, graph_min, graph_max, False)

    def display_svg(self, name):
        self.ax.clear()
        self.spectra[name].status = not self.spectra[name].status
        self.sig_switch.emit(self.spectra)
        empty = True
        for key in self.spectra.keys():
            if self.spectra[key].status:
                empty = False
                x = self.spectra[key].x
                y = self.spectra[key].y
                self.ax.plot(x, y, label=key)
                self.ax.set_xlabel('wavelength [nm]')
        self.ax.set_visible(not empty)
        self.ax.figure.canvas.draw()

