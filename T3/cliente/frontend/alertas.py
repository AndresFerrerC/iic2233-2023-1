
from PyQt5.QtWidgets import QMessageBox


def notificar(texto: str, tipo: str) -> None:
    """Retorna una alerta con contenido 'texto'
    del tipo 'tipo'; Warning, Information, etc."""
    box_alerta = QMessageBox()
    if tipo == "warning":
        box_alerta.setIcon(QMessageBox.Warning)
    else:
        box_alerta.setIcon(QMessageBox.Information)  # Por defecto
    box_alerta.setText(texto)
    box_alerta.setWindowTitle("Alerta")  # <- Se ignora en MacOS
    box_alerta.exec()
