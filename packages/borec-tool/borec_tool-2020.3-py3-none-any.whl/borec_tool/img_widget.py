from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QToolBar, QToolButton, \
    QMenu, QAction, QButtonGroup, QActionGroup
from PyQt5.QtGui import QImage

from borec_tool.gui.band_slider import Slider
from .gui.ndarray2pixmap import ndarray2pixmap
from .spectrum_window import SpectrumWindow
from borec_tool.gui.viewer import Viewer
from numpy import ndarray
import numpy as np
from pkg_resources import resource_filename
from .gui.selection import Mode


class ImgWindow(QWidget):

    mode_preview = True
    preview = None
    data = None
    band = 0

    ICON_DIR = 'borec_tool.resources.gui'

    slider_hide = pyqtSignal(bool)
    bands_sig = pyqtSignal(list)
    cube_sig = pyqtSignal(ndarray)

    def menu_action_triggered(self, item):
        self.img_selector.setDefaultAction(item)
        self.mode_preview = item.sender().text() == 'Preview'
        self.slider_hide.emit(self.mode_preview)
        if self.mode_preview:
            self.view.display_image(self.preview)
        else:
            self.display_raw(self.band)

    def _selection_triggered(self, status):
        self.view.set_sel_mode(status)
        self.spectrum.set_clear(status)

    def __init__(self, parent=None):
        QWidget.__init__(self)
        toolbar = QToolBar('Markers')
        stylesheet = 'QToolButton{width: 120; height: 20; margin: 1}'
        toolbar.setStyleSheet(stylesheet)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        images = QMenu()
        preview = QAction('Preview', images)
        preview.triggered.connect(lambda chck, item=preview: self.menu_action_triggered(item))
        cube = QAction('Spectral', images)
        cube.triggered.connect(lambda chck, item=cube: self.menu_action_triggered(item))
        images.addAction(preview)
        images.addAction(cube)
        img_selector = QToolButton(self)
        img_selector.setMenu(images)
        img_selector.setDefaultAction(preview)
        img_selector.setPopupMode(QToolButton.InstantPopup)
        self.img_selector = img_selector

        self.spectrum = SpectrumWindow(sel_status=Mode.SINGLE)
        view = Viewer(self)
        self.bands_sig.connect(self.spectrum.set_bands)
        self.cube_sig.connect(self.spectrum.set_cube)
        view.pos.connect(self.spectrum.draw_spectrum_at_pos)

        def set_action(status, icon=None, text=None):
            if icon is not None:
                action = QAction(QIcon(resource_filename(self.ICON_DIR, icon)),
                                      text, self)
            else:
                action = QAction(text, self)
            action.setCheckable(True)
            action.triggered.connect(lambda state, status=status: self._selection_triggered(status))
            return action

        toolbar.addWidget(img_selector)
        action_grp = QActionGroup(self)
        action_grp.setExclusive(True)

        single_mark = set_action(Mode.SINGLE, icon='cursor-cross.png', text='Single mark')
        single_mark.setChecked(True)
        action_grp.addAction(single_mark)
        toolbar.addAction(single_mark)

        multi_mark = set_action(Mode.MULTI, icon='multi-cross.png', text='Multiple marks')
        action_grp.addAction(multi_mark)
        toolbar.addAction(multi_mark)

        rect_mark = set_action(Mode.RECT, text='Rectangle')
        action_grp.addAction(rect_mark)
        toolbar.addAction(rect_mark)

        view.setMinimumHeight(512)
        self.spectrum.setMinimumWidth(512)
        self.view = view
        images = QWidget()
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(view)
        graph_layout.addWidget(self.spectrum)
        images.setLayout(graph_layout)
        self.images = images

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(images)
        slider = Slider(set_hidden=True)
        slider.band_idx.connect(self.display_raw)
        layout.addWidget(slider)
        self.slider = slider
        self.slider_hide.connect(slider.setHidden)
        self.setLayout(layout)

    def display_image(self):
        self.view.display_image()

    def set_data(self, data):
        self.data = data
        self.preview = data.preview
        cube = data.reflectance.data
        self.cube_max = np.max(cube)
        self.cube = cube
        self.bands = data.reflectance.header.bands.centers
        self.bands_sig.emit(self.bands)
        self.cube_sig.emit(self.cube)
        self.view.set_image(self.preview)
        self.slider.values = self.bands
        if self.mode_preview:
            self.view.display_image()
        else:
            self.display_raw()

    def set_bands(self, bands):
        self.bands_sig.emit(bands)

    def get_pixmap(self, band):
        image = self.cube[:,:,band]
        image = np.uint8(image/np.float(self.cube_max)*255)
        return ndarray2pixmap(image, format=QImage.Format_Grayscale8)

    def display_raw(self, band=None):
        if band is not None:
            self.band = band
        if self.data is not None:
            self.view.display_image(self.get_pixmap(self.band))

    def save(self):
        return

