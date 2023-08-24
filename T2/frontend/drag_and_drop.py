from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class BotonMovible(QPushButton):
    def __init__(self, texto: str, parent: object, nombre: str) -> None:
        super().__init__(texto, parent)
        self.nombre = nombre

    def setear_pixmap(self, pixmap) -> None:
        """Define el pixmap del botón"""
        self.pixmap = pixmap

    def mouseMoveEvent(self, event) -> None:
        """Define el evento del Drag and Drop"""
        if event.buttons() == Qt.LeftButton:
            mimedata = QMimeData()
            drag = QDrag(self)
            drag.setPixmap(self.pixmap)

            drag.setMimeData(mimedata)
            mimedata.setText(self.nombre)
            dropAction = drag.exec_(Qt.MoveAction)
