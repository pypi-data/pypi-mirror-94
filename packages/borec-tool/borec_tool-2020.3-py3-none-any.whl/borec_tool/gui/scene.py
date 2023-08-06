from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPointF, QRectF, pyqtSignal, QPoint
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsItem
from PyQt5.QtWidgets import QGraphicsPixmapItem
from borec_tool.gui.selection import Mode

class Scene(QGraphicsScene):

    pos = pyqtSignal(object)
    pixmap = None

    def __init__(self, mode):
        super(Scene, self).__init__()
        self.mode = mode
        self.crosshair = QtGui.QPixmap('borec_tool/resources/gui/cursor-cross.png')
        self.cursor_center = self.crosshair.rect().center()
        self.markers = []

    def set_select_mode(self, mode):
        self.mode = mode
        if mode == Mode.SINGLE:
            self._remove_markers()

    def setCursorPos(self, cursorPos):
        if self.mode == Mode.SINGLE and self.markers:
            self._remove_markers()
        cursor = QGraphicsPixmapItem(self.crosshair)
        cursor.setPos(cursorPos-self.cursor_center)
        cursor.setZValue(1)
        self.markers.append(cursor)
        self.addItem(cursor)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.pixmap is not None:
            # set the current position and schedule a repaint of the label
            cursorPos = event.scenePos().toPoint()
            if self.mode != Mode.RECT:
                self.setCursorPos(cursorPos)
                self.pos.emit(cursorPos)
            if self.mode == Mode.RECT:
                self._start_point = event.scenePos()
                self._rectangle = Rectangle(self._start_point)
                self._rectangle.setZValue(1)
                self.markers.append(self._rectangle)
                self.addItem(self._rectangle)
        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.pixmap is not None:
            if self.mode == Mode.RECT and hasattr(self, '_rectangle'):
                    self._rectangle.setRect(QRectF(self._start_point, event.scenePos()).normalized())
            else:
                super(Scene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if self.pixmap is not None:
            if self.mode == Mode.RECT and hasattr(self, '_rectangle'):
                self.pos.emit(self._rectangle)
            else:
                super(Scene, self).mouseReleaseEvent(event)


    def _remove_markers(self):
        for marker in self.markers:
            self.removeItem(marker)
        self.markers = []

    def set_image(self, image):
        if self.pixmap is not None:
            self.removeItem(self.pixmap)
        pixmap = self.addPixmap(image)
        rect = self.itemsBoundingRect()
        self.setSceneRect(rect)
        pixmap.setZValue(0)
        self.pixmap = pixmap



class Rectangle(QGraphicsRectItem):
    def __init__(self, point):
        super(Rectangle, self).__init__(QRectF(point, point))
        self.setPen(QtGui.QPen(QtCore.Qt.white, 2))
        self.setFlags(QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges)

    def mouseMoveEvent(self, e):
        if e.buttons() & QtCore.Qt.LeftButton:
            self.setRect(QtCore.QRectF(QtCore.QPoint(), e.pos()).normalized())
        if e.buttons() & QtCore.Qt.RightButton:
            super(Rectangle, self).mouseMoveEvent(e)

    def itemChange(self, change, val):
        if change == QGraphicsItem.ItemPositionChange | change == QGraphicsItem.ItemScaleChange:
            return QPointF(val.x(), val.y())
        return val