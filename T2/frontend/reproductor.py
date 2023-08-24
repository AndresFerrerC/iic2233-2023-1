from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from parametros import PATH_WIN_MP3, PATH_LOSS_MP3
import os


class Reproductor(QObject):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.reproductor = QMediaPlayer()
        self.instalar_media()

    def instalar_media(self) -> None:
        """Instala los archivos de audio WIN/LOSS"""
        path_win_mp3 = os.path.abspath(os.path.join(*PATH_WIN_MP3))
        self.archivo_win = QUrl.fromLocalFile(path_win_mp3)
        self.contenido_win = QMediaContent(self.archivo_win)
        # Audio de Loss
        path_loss_mp3 = os.path.abspath(os.path.join(*PATH_LOSS_MP3))
        self.archivo_loss = QUrl.fromLocalFile(path_loss_mp3)
        self.contenido_loss = QMediaContent(self.archivo_loss)

    def reproducir_audio(self, tipo: str) -> None:
        """Reproduce audio del tipo WIN/LOSS"""
        if tipo == "WIN":
            self.reproductor.setMedia(self.contenido_win)
        else:
            self.reproductor.setMedia(self.contenido_loss)
        self.reproductor.play()
