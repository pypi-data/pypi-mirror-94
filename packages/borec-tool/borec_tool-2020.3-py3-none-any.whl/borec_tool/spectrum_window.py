import matplotlib

from PyQt5.QtCore import pyqtSlot, QPoint
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg)

from matplotlib.figure import Figure
import numpy as np
from .gui.selection import Mode
from .gui.scene import Rectangle
from .data_utilities.statistics import quantiles

matplotlib.use("Qt5Agg", force=True)


class SpectrumWindow(FigureCanvasQTAgg):
    position = []
    elements = []
    cube = None
    bands = None
    max = None

    def __init__(self, sel_status=Mode.SINGLE):

        self.sel_status = sel_status
        fig = Figure(figsize=(10, 5))
        FigureCanvasQTAgg.__init__(self, fig)
        self._fig = fig
        self._ax = fig.canvas.figure.subplots()
        fig.set_visible(False)

    def set_bands(self, bands):
        self.bands = np.array(bands)

    def set_cube(self, cube):
        self.cube = cube
        self.max = np.ceil(np.max(cube)*10)/10
        if self.position:
            self._ax.clear()
            self.draw_spectrum_at_pos(self.position)

    def draw_data(self):
        if self.position:
            self._ax.clear()
            self.draw_spectrum_at_pos(self.position)

    @pyqtSlot(Mode)
    def set_clear(self, clear):
        self.sel_status = clear
        if clear != Mode.MULTI:
            self._ax.clear()
            self._ax.figure.canvas.draw()

    def draw_spectrum_at_pos(self, position):
        if self.cube is not None:
            x = self.bands
            self._fig.set_visible(True)
            values = []
            if isinstance(position, QPoint):
                pos_x = position.x()
                pos_y = position.y()
                values = [self.cube[pos_x][pos_y]]
            elif isinstance(position, Rectangle):
                stats = quantiles(self.cube, position)
                values = (stats['quantile-0'].to_numpy(),
                          stats['quantile-1'].to_numpy(),
                          stats['quantile-2'].to_numpy())
            if not isinstance(position, list):
                position = [position]
            if self.sel_status == Mode.SINGLE:
                self.position = position
                self.elements = [values]
            else:
                self.position.extend(position)
                self.elements.append(values)
                # convert positioin to list
            if self.sel_status == Mode.SINGLE:
                self._ax.clear()
            self._ax.set_xlabel('wavelength [nm]')
            for elem in self.elements:
                if isinstance(elem, list):
                    self._ax.plot(x, np.squeeze(elem))
                else:
                    self._ax.plot(x, elem[1], label='median')
                    self._ax.fill_between(x, elem[0], elem[2], alpha=0.2, label='q25-q75')
            self._ax.set_xlabel('wavelength [nm]')
            self._ax.set_ylim([0, self.max])
            # pos_x = self.position[-1].x()
            # pos_y = self.position[-1].y()
            # self._ax.title.set_text('Spectrum for coordinates: x = {}, y = {}'.format(pos_x, pos_y))
            self._ax.title.set_text('Image spectrum')
            self._ax.figure.canvas.draw()
            self.show()

    def draw_vectors(self, vectors):
        x = self.bands
        self._fig.set_visible(True)
        self._ax.clear()
        self._ax.plot(x, vectors.transpose())
        self._ax.figure.canvas.draw()
        self.show()
