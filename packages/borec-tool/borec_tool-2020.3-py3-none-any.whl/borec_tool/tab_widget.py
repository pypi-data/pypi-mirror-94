from PyQt5.QtWidgets import QTabWidget, QWidget, QTabBar, QGridLayout, \
    QMessageBox
from PyQt5.QtCore import pyqtSignal

from .img_widget import ImgWindow
from .led_lighting import Led
from .radiance import Radiance
from .data_utilities.cube import DataHdr
from .data_utilities.saver import Saver

class SpectralTabs(QTabWidget):

    bands_sig = pyqtSignal(list)
    reflect_sig = pyqtSignal(DataHdr)

    def __init__(self, parent=None):
        QTabWidget.__init__(self)
        self.saver = Saver()
        self.setTabsClosable(True)
        # create widgets
        self.tab_image = ImgWindow(parent=self)
        # self.tab_statistics = QWidget()
        self.tab_led = QWidget()
        self.tab_radiance = QWidget()

        # Add tabs
        self.addTab(self.tab_image, "Image")
        # self.addTab(self.tab_statistics, "Statistics")
        self.addTab(self.tab_led, "Illumination")

        for idx in range(2):
            self.tabBar().setTabButton(idx, QTabBar.RightSide, None)
        self.tabCloseRequested.connect(lambda idx: self.closeTab(idx))


        # self.tab_statistics.layout = QHBoxLayout(self)
        self.tab_led.layout = QGridLayout()
        self.tab_radiance.layout = QGridLayout()

        self.led = Led()
        self.tab_led.layout.addWidget(self.led)

        self.radiance = Radiance()
        self.tab_radiance.layout.addWidget(self.radiance)
        self.radiance.sig_tab.connect(self.radiance_window)

        # self.tab_statistics.setLayout(self.tab_statistics.layout)
        self.tab_led.setLayout(self.tab_led.layout)
        self.tab_radiance.setLayout(self.tab_radiance.layout)

    def closeTab(self, idx):
        self.removeTab(idx)
        self.setCurrentWidget(self.tab_image)

    def update_display(self, data):
        self.full_data = data
        self.bands = data.reflectance.header.bands.centers
        reflectance = data.reflectance.data
        self.data_size = reflectance.shape[-1]
        self.tab_image.set_data(data)
        self.bands_sig.emit(self.bands)
        self.radiance.set_data(data)

    def tab_window(self, cls, tab_name, **kwargs):
        tab = cls(parent=self, **kwargs)
        self.addTab(tab, tab_name)
        self.setCurrentWidget(tab)
        self.reflect_sig.connect(tab.process)
        self.reflect_sig.emit(self.full_data.reflectance)

    def radiance_window(self):
        self.addTab(self.tab_radiance, "Radiance")

    def set_directory(self, directory):
        self.directory = directory
        self.saver.dir = directory

    def save_as_slot(self):
        if hasattr(self.currentWidget(), 'output'):
            filename = self.saver.save_as(self.currentWidget().output)
        else:
            QMessageBox.information(self,'Info','Function has no output to save')

    def save_slot(self):
        if hasattr(self.currentWidget(), 'output'):
            filename = self.saver.save(self.currentWidget().output)
        else:
            QMessageBox.information(self,'Info','Function has no output to save')

