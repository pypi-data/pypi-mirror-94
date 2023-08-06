from __future__ import absolute_import
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QAction, QSplitter, QGridLayout, QWidget,
                             QMenuBar, QVBoxLayout, QListWidget, QMessageBox, QFileDialog)
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from docutils.nodes import image

from borec_tool.data_utilities.loader import open_folder
from .data_utilities import loader as loader
from .clustering import Clustering
from borec_tool.gui.parameters import SpinBoxParams, StringBoxParams
from .bands_browser_with_graph import BandsBrowserWithGraph
from .data_utilities.cube import Hyperspectral, DataHdr
from pathlib import Path
from .img_sigma import Sigma
from .processing import KMeans, MiniBatchKMeans, PCA_KMeans, PCA_HDBSCAN, bilateral
from .img_quantiles import Quantiles
from .tab_widget import SpectralTabs
from numpy import ndarray
import skimage
from .img_pca import EvalPCA

import sys


class ListSlider(QtWidgets.QSlider):
    elementChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, values=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(0)
        self._values = []
        self.valueChanged.connect(self._on_value_changed)
        self.values = values or []

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values
        maximum = max(0, len(self._values) - 1)
        self.setMaximum(maximum)
        self.setValue(0)

    @QtCore.pyqtSlot(int)
    def _on_value_changed(self, index):
        value = self.values[index]
        self.elementChanged.emit(index, value)

class MainWindow(QMainWindow):
    MaxRecentFiles = 5
    bands_sig = pyqtSignal(list)
    reflect_sig = pyqtSignal(DataHdr)
    sig_data = pyqtSignal(ndarray)
    sig_dir = pyqtSignal(Path)
    # full_data_sig = pyqtSignal(dict)
    data_hyperspectral_sig = pyqtSignal(Hyperspectral)

    def __init__(self):
        QMainWindow.__init__(self)
        self.recentFileActs = []

        main_window = QWidget()

        # Navbar
        navbarLayout = QGridLayout()
        # Buttons
        openfolder_button = QAction("Open folder", self)
        close_button = QAction("Close", self)
        # Actions of buttons
        openfolder_button.triggered.connect(self.menu_open_folder)
        close_button.triggered.connect(self.close)
        # Create menu
        #menubar = QMenuBar()
        menubar = self.menuBar()
        navbarLayout.addWidget(menubar, 0, 0)
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(openfolder_button)
        # recent files
        recent_file = fileMenu.addMenu("Open recent")
        self.createRecentFileActions()
        for i in range(self.MaxRecentFiles):
            recent_file.addAction(self.recentFileActs[i])
        self.updateRecentFileActions()
        save_file = QAction("&Save", self)
        save_file.setShortcut("Ctrl+S")
        save_file.setStatusTip('Save File')
        save_as = QAction("Save as", self)
        fileMenu.addAction(save_file)
        fileMenu.addAction(save_as)
        fileMenu.addSeparator()
        fileMenu.addAction(close_button)
        fcn_menu = menubar.addMenu("Functions")
        self.fcn_menu = fcn_menu
        menu_sigma = QAction("Data mean", self)
        menu_sigma.setEnabled(False)
        menu_sigma.triggered.connect(lambda status: self.menu_tabs.tab_window(Sigma, "Data mean"))
        fcn_menu.addAction(menu_sigma)
        self.menu_sigma = menu_sigma

        menu_quartiles = QAction("Quantiles", self)
        menu_quartiles.setEnabled(False)
        menu_quartiles.triggered.connect(lambda status: self.menu_tabs.tab_window(Quantiles, "Quantiles"))
        fcn_menu.addAction(menu_quartiles)
        self.menu_sigma = menu_sigma


        menu_clustering = QAction("KMeans", self)
        menu_clustering.setEnabled(False)
        params = {'n_clusters': SpinBoxParams(max=99, value=5, label="N clusters: "),
                  'max_iter': SpinBoxParams(max=999, value=100, step=100, label="N iterations: ")}
        menu_clustering.triggered.connect(lambda status: self.menu_tabs.tab_window(Clustering, "KMeans",
                                                                         clusterer=KMeans, parameters=params))
        fcn_menu.addAction(menu_clustering)

        menu_minibatch = QAction("Mini-Batch KMeans", self)
        menu_minibatch.setEnabled(False)
        menu_minibatch.triggered.connect(lambda status: self.menu_tabs.tab_window(Clustering, "Mini-Batch KMeans",
                                                                        clusterer=MiniBatchKMeans, parameters=params))
        fcn_menu.addAction(menu_minibatch)

        menu_pca_kmeans = QAction("PCA-KMeans", self)
        menu_pca_kmeans.setEnabled(False)
        params_pca_km = {'n_components': SpinBoxParams(max=10, value=2, label="N components"),
                  'n_clusters': SpinBoxParams(max=99, value=5, label="N clusters: "),
                  'max_iter': SpinBoxParams(max=999, value=100, step=100, label="N iterations: ")}
        menu_pca_kmeans.triggered.connect(lambda: self.menu_tabs.tab_window(Clustering, "PCA-KMeans",
                                                                        clusterer=PCA_KMeans, parameters=params_pca_km))
        fcn_menu.addAction(menu_pca_kmeans)

        params_pca_dbscan = {'n_components':
                                 SpinBoxParams(max=100,
                                               value=5,
                                               label="N components"
                                               ),
                             'min_cluster_size':
                                 SpinBoxParams(max=30000,
                                               value=1000,
                                               step=100,
                                               label="Min cluster size")
                             }
        menu_dbscan = QAction("PCA HDBSCAN", self)
        menu_dbscan.setEnabled(False)
        menu_dbscan.triggered.connect(
            lambda: self.menu_tabs.tab_window(Clustering,
                                              "PCA HDBSCAN",
                                              clusterer=PCA_HDBSCAN,
                                              parameters=params_pca_dbscan)
        )
        fcn_menu.addAction(menu_dbscan)


        menu_pca = QAction("PCA", self)
        menu_pca.setEnabled(False)
        menu_pca.triggered.connect(lambda: self.menu_tabs.tab_window(EvalPCA, "PCA"))
        fcn_menu.addAction(menu_pca)

        par_wavelet = {'wavelet':
                          StringBoxParams(
                              values=['db1', 'db2', 'haar'],
                              label='Wavelet: '
                          ),
                      'mode':
                          StringBoxParams(
                              values=['soft', 'hard'],
                              label='Mode: '
                          ),
                      'method':
                          StringBoxParams(
                              values=['BayesShrink', 'VisuShrink'],
                              label='Method: '
                          )
        }
        menu_wavelet = QAction("Wavelet denoising", self)
        menu_wavelet.setEnabled(False)
        menu_wavelet.triggered.connect(lambda status:
                                       self.menu_tabs.tab_window(BandsBrowserWithGraph, "Wavelet",
                                                                 fun=skimage.restoration.denoise_wavelet, parameters=par_wavelet))
        fcn_menu.addAction(menu_wavelet)

        par_bilateral = {'win_size':
                                 SpinBoxParams(max=30,
                                               value=1,
                                               label="Win size"
                                               ),
                             'sigma_spatial':
                                 SpinBoxParams(max=20,
                                               value=1,
                                               step=1,
                                               label="Stddev spatial")
                             }
        menu_bilateral = QAction("Bilateral filter", self)
        menu_bilateral.setEnabled(False)
        menu_bilateral.triggered.connect(
            lambda: self.menu_tabs.tab_window(BandsBrowserWithGraph,
                                              "Bilateral",
                                              fun=bilateral,
                                              parameters=par_bilateral)
        )
        fcn_menu.addAction(menu_bilateral)


        help_menu = menubar.addMenu("Help")
        about = QAction("About", self)
        about.triggered.connect(self.about_box)
        help_menu.addAction(about)

        self.menu_tabs = SpectralTabs(parent=self)
        self.sig_dir.connect(self.menu_tabs.set_directory)
        self.reflect_sig.connect(self.menu_tabs.reflect_sig)
        self.data_hyperspectral_sig.connect(self.menu_tabs.update_display)
        save_file.triggered.connect(lambda: self.menu_tabs.save_slot())
        save_as.triggered.connect(lambda: self.menu_tabs.save_as_slot())

        self.menu_tabs.led.sig_radiance.connect(self.menu_tabs.radiance.set_illumination)

        list_splitter = QSplitter()

        self.opened_listwidget = QListWidget(parent=self)
        self.opened_listwidget.itemClicked.connect(
            lambda item: self.menu_open_folder(Path(item.text()), add_to_open=False))
        list_splitter.addWidget(self.opened_listwidget)

        main_splitter = QSplitter()
        main_splitter.addWidget(list_splitter)

        imageLayout = QVBoxLayout()
        # imageLayout.addWidget(self.toolbar)
        imageLayout.addWidget(self.menu_tabs)
        imageLayout.setContentsMargins(0, 0, 0, 0)
        image = QWidget()
        image.setLayout(imageLayout)
        # File browser
        main_splitter.addWidget(image)

        # Layouts
        mainLayout = QVBoxLayout()

        mainLayout.addLayout(navbarLayout)
        mainLayout.addWidget(main_splitter)
        main_window.setLayout(mainLayout)
        self.setCentralWidget(main_window)
        self.setGeometry(50, 50, 1400, 540)
        self.setWindowTitle('BOREC tool')
        self.show()

    def createRecentFileActions(self):
        self.files = loader.load_history()
        for i in range(self.MaxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False,
                        triggered=self.openRecentFile))

    def updateRecentFileActions(self):
        numRecentFiles = min(len(self.files), self.MaxRecentFiles) if self.files else 0

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, Path(self.files[i]).name)
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(self.files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, self.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.menu_open_folder(directory=Path(action.data()))

    def update_recent(self):
        try:
            self.files.remove(str(self.directory))
        except (ValueError):
            pass

        self.files.insert(0, str(self.directory))
        del self.files[self.MaxRecentFiles:]

        loader.save_history(self.files)
        self.updateRecentFileActions()

    def about_box(self):
        msg = QMessageBox()
        text = 'The development of this software has been supopported\n' \
                'by the Technology Agency of the Czech Republic\n'\
                'grant No. TH03010330\n' \
                '\n' \
                'The tool is licensed under the BSD-3 license\n\n' \
                'For the source code, please contact\nJan Schier\n' \
                'Instute of Information Theory and Automation\n' \
                'Department of Image Processing\n' \
                'schier@uta.cas.cz\n'

        msg.setText(text)
        msg.setWindowTitle('Info')
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec()

    def get_dir(self, dir=None):
        selected = QFileDialog.getExistingDirectory(caption='Select directory with image data',
                                                     directory=dir)
        if not selected: raise Exception()
        return Path(selected)

    def menu_open_folder(self, directory=None, add_to_open=True):
        try:
            self.directory = self.get_dir() if not directory else directory
        except Exception as e:
            return
        self.sig_dir.emit(self.directory)
        full_data = open_folder(self.directory)
        if full_data:
            self.reflect_sig.emit(full_data.reflectance)
            self.menu_tabs.full_data_obj = full_data
            self.data_hyperspectral_sig.emit(full_data)
            self.update_recent()
            if add_to_open:
                self.opened_listwidget.addItem(str(self.directory))
            for action in self.fcn_menu.actions():
                action.setEnabled(True)

    def get_data(self, spectra_all):
        if hasattr(self, 'full_data'):
            self.sig_data.emit(spectra_all)
            self.menu_tabs.addTab(self.menu_tabs.tab_radiance, "Radiance")


def main():
    app = QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()