from PyQt5.QtCore import QFile, QFileInfo, QIODevice, QUrl, QDataStream, QBuffer, QByteArray
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    player = QMediaPlayer()

    file = QFile('/Users/junahyung/emomovie/SimpsonSen.mp4')

    print(1)
    isOpen = file.open(QIODevice.ReadOnly)
    print(2)

    buffer = QBuffer()
    buffer.open(QIODevice.ReadWrite)
    print(3)

    player.setMedia(QMediaContent(), buffer)
    print(4)

    if isOpen:
        while not file.atEnd():
            temp = file.readLine()
            # temp = QByteArray.fromBase64(temp)
            buffer.write(temp)

    print(5)
    videoWidget = QVideoWidget()
    print(6)
    player.setVideoOutput(videoWidget)
    print(7)
    videoWidget.show()
    print(8)

    player.play()
    while(player.MediaStatus()==QMediaPlayer.UnknownMediaStatus):
        print("a")
    print(9)
    sys.exit(app.exec_())
