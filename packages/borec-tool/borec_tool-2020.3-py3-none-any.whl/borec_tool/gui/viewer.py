from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QEvent
from PyQt5 import QtGui

from borec_tool.gui.scene import Scene, Rectangle
from borec_tool.gui.selection import Mode


class Viewer(QGraphicsView):
    pos = pyqtSignal(object)
    clear = pyqtSignal(Mode)
    pixmap = None

    def __init__(self, parent=None):
        QGraphicsView.__init__(self)
        self.setWindowTitle("scene")
        self.setStyleSheet("border: 0px")
        self.sel_mode = Mode.SINGLE
        self.scene = Scene(self.sel_mode)
        self.scene.pos.connect(self.pos)

        self.setScene(self.scene)
        self.setMinimumSize(512,512)
        self.setGeometry(0,0,512,512)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.installEventFilter(self)

    def set_image(self, image):
        self.scene.set_image(image)
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.viewport().setCursor(Qt.CrossCursor)

    def display_image(self, image=None):
        if image is not None:
            self.scene.set_image(image)
        self.show()

    def set_sel_mode(self, selected):
        self.scene.set_select_mode(selected)
        self.clear.emit(selected)

