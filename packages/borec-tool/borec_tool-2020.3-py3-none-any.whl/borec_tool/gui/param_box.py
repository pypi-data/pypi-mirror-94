from PyQt5.QtWidgets import QSpinBox, QComboBox


class SpinBox(QSpinBox):

    def __init__(self, key, param, parent=None):
        QSpinBox.__init__(self)
        self.setRange(param.min, param.max)
        self.setSingleStep(param.step)
        self.setValue(param.value)
        self.key = key


class StringBox(QComboBox):
    def __init__(self, param, parent=None):
        super(StringBox, self).__init__(parent)
        self.addItems(param)