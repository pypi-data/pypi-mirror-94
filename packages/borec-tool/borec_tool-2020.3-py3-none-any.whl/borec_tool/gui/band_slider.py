from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QLCDNumber, QHBoxLayout, QSlider, QLabel
from PyQt5.QtGui import QFont

class Slider(QFrame):

    display_raw = pyqtSignal(float)
    band_idx = pyqtSignal(int)
    index = 0

    def __init__(self, set_hidden=False):
        QFrame.__init__(self)
        sp = self.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self.setSizePolicy(sp)
        self.setHidden(set_hidden)
        wave_slider = ListSlider(orientation=QtCore.Qt.Horizontal)
        #wave = QLCDNumber(self)
        wave = QLabel()
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        wave.setFont(font)
        # wave.setFrameShape(QFrame.Panel)

        wave.setFixedWidth(80)
        self.wave = wave

        wave_slider.elementChanged.connect(self.my_list_slider_valuechange)
        wave_slider.valueChanged.connect(
            lambda band=wave_slider.value(): self.display_raw.emit(band))
        wave_slider.valueChanged.connect(
            lambda band=wave_slider.value(): self.band_idx.emit(band)
        )
        self.wave_slider = wave_slider

        #self.setMinimumWidth(512)
        layout = QHBoxLayout()
        layout.addWidget(wave_slider)
        layout.addWidget(wave)
        self.setLayout(layout)

    def my_list_slider_valuechange(self, index, value):
        self.index = index
        val = self.wave_slider.values[index]
        self.wave.setText(f'{val:>8.2f} nm')


    @property
    def values(self):
        return self.wave_slider.values

    @values.setter
    def values(self, values):
        self.wave_slider.values = values
        self.my_list_slider_valuechange(self.index, values[self.index])


class ListSlider(QSlider):
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