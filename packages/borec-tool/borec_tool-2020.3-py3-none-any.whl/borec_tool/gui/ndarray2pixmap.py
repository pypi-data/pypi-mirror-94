from PyQt5.QtGui import QImage, QPixmap

def ndarray2pixmap(data, format=QImage.Format_RGB888):
    return QPixmap(QImage(data.tobytes(), *data.shape[0:2][::-1], data[0, :].nbytes, format))