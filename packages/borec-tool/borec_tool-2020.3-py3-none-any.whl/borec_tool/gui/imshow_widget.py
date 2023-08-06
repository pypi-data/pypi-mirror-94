from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.cm as cm

from PyQt5.QtWidgets import QSizePolicy


class ShowImage(FigureCanvas):

    def __init__(self, parent=None, width=10, height=8):
        fig = Figure(figsize=(width, height))
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)

        self._fig = fig
        self._ax = fig.canvas.figure.subplots()
        fig.set_visible(False)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def img_show(self, data, **kwargs):
        self._ax.clear()
        self._ax.imshow(data, **kwargs)
        self._ax.axis('off')
        self._fig.set_visible(True)
        self._ax.figure.canvas.draw()
        self.show()