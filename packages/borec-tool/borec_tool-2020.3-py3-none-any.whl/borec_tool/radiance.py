from PyQt5.QtWidgets import (QApplication, QColumnView, QAction, QFileSystemModel, QSplitter, QTreeView, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox,
                             QWidget,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout, QSlider, QListWidget)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from matplotlib.figure import Figure
import sys
import numpy as np
from scipy import interpolate
import scipy.io

from .gui.ndarray2pixmap import ndarray2pixmap
from borec_tool.gui.viewer import Viewer
from pkg_resources import resource_filename


class Radiance(QWidget):
    sig_tab = pyqtSignal()

    def __init__(self):
        super(Radiance, self).__init__()
        self.radiance_layout = QVBoxLayout()

        view = Viewer(self)
        self.view = view
        self.radiance_layout.addWidget(self.view)
        self.xyzbar = scipy.io.loadmat(resource_filename('borec_tool.resources', 'xyzbar_interpolated.mat'))

        self.setLayout(self.radiance_layout)


    def XYZ2sRGB_exgamma(self, XYZ):
        d = XYZ.shape
        M = np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0414], [0.0557, -0.2040, 1.0570]])
        XYZ_new = np.reshape(XYZ, [d[0] * d[1], d[2]])
        sRGB = (np.dot(M, XYZ_new.transpose())).transpose()
        sRGB_res = np.reshape(sRGB, d)
        return sRGB_res

    def set_illumination(self, graph_data):
        self.graph_data = graph_data
        if hasattr(self, 'data'):
            self.radiance_data(self.data, graph_data)

    def set_data(self, data):
        self.data = data
        if hasattr(self, 'graph_data'):
            self.radiance_data(data, self.graph_data)

    def radiance_data(self, data, graph_data):
        step = 10
        bands_Forest_min = 400
        bands_Forest_max = 730
        svg_d = graph_data['y_scale']
        wavelength = np.array(data.reflectance.header.bands.centers)

        reflectance = data.reflectance.data

        x = np.arange(graph_data['x_scale'][0], graph_data['x_scale'][1])

        f = interpolate.interp1d(x, svg_d)
        # g = interpolate.interp1d(bands_Forest, xyzbar['xyzbar'].transpose())

        xnew = np.arange(graph_data['x_scale'][0], graph_data['x_scale'][1] - step, 0.01)
        svg_int = f(xnew)

        svg_inter = []
        xyzbar_inter = []

        for wave in wavelength:
            if wave < graph_data['x_scale'][0] or wave > (graph_data['x_scale'][1] - step):
                svg_inter.append(0)
            else:
                svg_inter.append(svg_int[int(100 * (wave - graph_data['x_scale'][0]))])

        for wave in wavelength:
            if wave < bands_Forest_min or wave > (bands_Forest_max - step):
                xyzbar_inter.append(np.array([0, 0, 0]))
            else:
                xyzbar_inter.append(self.xyzbar['xyzbar'][int(100 * (wave - bands_Forest_min))])

        svg = np.array(svg_inter)
        svg = svg[np.newaxis, np.newaxis, :]
        radiance = np.multiply(reflectance, svg)

        rcw = radiance.shape
        xyz_Specim = np.array(xyzbar_inter)
        radiance = np.reshape(radiance, [-1, rcw[2]])

        XYZ = (np.dot(xyz_Specim.transpose(), radiance.transpose())).transpose()
        XYZ = np.reshape(XYZ, [rcw[0], rcw[1], 3])
        if XYZ.max() != 0:
            XYZ = XYZ / XYZ.max()

        RGB = self.XYZ2sRGB_exgamma(XYZ)
        RGB_disp = np.clip(RGB, 0, 1)
        self.display_raw(RGB_disp)
        self.sig_tab.emit()

    def display_raw(self, data):
        data = np.uint8(data * 255)
        self.view.display_image(ndarray2pixmap(data))
        self.sig_tab.emit()

