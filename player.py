from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSignal, QPoint, QSize, QTime, QFile, QFileInfo, QDataStream, QBuffer, QByteArray, QIODevice, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QFrame)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QLCDNumber
from PyQt5.QtGui import * 
import sys
import os
import math
import json
import time

class VideoWindow(QMainWindow):
    pevent = pyqtSignal(float)
    def __init__(self, seqtxt, outputtxt, duration, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("[Emo Player] ")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        #videoWidget = QVideoWidget()
        self.lcd = QLCDNumber(self)
        self.duration = 1000*int(duration)
        self.lastwrite = 0
        self.coor = (0,0)

        self.lcdtime = QTimer()
        self.lcdtime.timeout.connect(self.lcdprint)
        self.lcdcnt = 5
        
        #json configuration
        with open("config.json", "r") as fp:
            config = json.load(fp)
        self.radius = config['radius'] 
        self.greentime = config['greentime'] 
        self.yellowtime = config['yellowtime'] 
        self.reco_freq = config['reco_freq']
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.time)

        self.state = 'stopped'
        self.position = 0
        self.seqtxt = seqtxt
        self.outputtxt = outputtxt

        self.genseq()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0,0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.duration /= 1000 
        self.positionSlider.setRange(0, self.duration)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.labelDuration = QLabel()

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(exitAction)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0,0,0,0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.labelDuration)

        layout = QVBoxLayout()
        layout.addWidget(self.lcd)
        #layout.addWidget(videoWidget,4)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        rwindow = Tracker(self)
        self.rlabel = QLabel(self)
        rwindow.newPoint.connect(self.setCoor)
        rwindow.clickPoint.connect(self.click_writeCoor)
        rlayout = QVBoxLayout()
        rlayout.addWidget(self.rlabel)
        rlayout.addWidget(rwindow)

        totalLayout = QHBoxLayout()
        totalLayout.addLayout(layout)
        totalLayout.addLayout(rlayout)

        wid.setLayout(totalLayout)


        #url = os.path.join(os.getcwd(), movietitle) 
        #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(url)))
        self.playButton.setEnabled(True)

    def time(self):
        self.position += 0.01 
        self.positionChanged()

    def changeCoor(self,x,y):
        x,y =  (self.radius*float(x-335)/237, self.radius*float(-1*(y-326))/237)
        if x**2 + y**2 > (self.radius+0.1)**2:
            theta = math.atan2(y,x)
            x = self.radius*math.cos(theta)
            y = self.radius*math.sin(theta)
        return (x,y)

    def setCoor(self, event):
        self.coor = self.changeCoor(event.x(), event.y())
        self.rlabel.setText('Coordinates: ( %f : %f )' % (self.coor))

    def click_writeCoor(self, event):
        x, y = self.changeCoor(event.x(), event.y())
        line = "%f %f %f\n" % (x, y, self.position) 
        fileName = self.changeFileName(self.outputtxt, "clicked")
        with open(fileName, 'a') as fp:
            fp.write(line)

    def target_writeCoor(self):
        x, y = self.coor 
        line = "%f %f %f\n" % (x, y, self.position) 
        fileName = self.changeFileName(self.outputtxt, "target")
        with open(fileName, 'a') as fp:
            fp.write(line)

    @staticmethod
    def changeFileName(ori, new):
        split = ori.split('.')
        split.insert(-1, '_' + new)
        ext = split.pop()
        name = ''.join(split) + '.' + ext
        return name


    def keyPressEvent(self, event):
        key = event.key()
        self.play()


    def exitCall(self):
        sys.exit(app.exec_())

    def lcdprint(self):
        self.lcd.display(self.lcdcnt) 
        if 1<=self.lcdcnt and self.lcdcnt<= 5:
            self.lcdcnt = self.lcdcnt -1
        else:
            self.lcdcnt = 5
            self.state = 'playing'
            self.statusBar().showMessage('playing')
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.timer.start(10)
            self.lcdtime.stop()
            
    def play(self):
        if self.state == 'playing':
            self.state = 'paused'
            self.statusBar().showMessage('paused')
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()

        else:
            #self.lcdtime.connect(self.lcd)
            self.lcdtime.start(1000)
            self.lcdtime.start(1000)
            self.lcdtime.start(1000)
            self.lcdtime.start(1000)
            self.lcdtime.start(1000)



    def positionChanged(self):
        self.pevent.emit(self.position)
        self.positionSlider.setValue(self.position)
        self.updateDurationInfo(self.position)

        if int(self.position) in self.greentarget and int(self.position) % self.reco_freq == 0 and self.lastwrite < int(self.position):
            self.target_writeCoor()
            self.lastwrite = self.position

    def updateDurationInfo(self, currentInfo):
        duration = self.duration
        if currentInfo or duration:
            currentTime = QTime((currentInfo/3600) % 60, (currentInfo/60) % 60, currentInfo % 60, (currentInfo*1000)%1000)
            totalTime = QTime((duration/3600) % 60, (duration/60) % 60, duration % 60, (duration*1000)%1000)
            format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
            tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
        else:
            tStr = "" 
        self.labelDuration.setText(tStr)

    def durationChanged(self, duration):
        duration /= 1000 
        self.positionSlider.setRange(0, duration)
        self.duration = duration

    def setPosition(self, position):
        self.position = position

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def genseq(self):
        with open(self.seqtxt, 'r') as fp:
            line = fp.readline()
            line = line.split()
            line = [int(e) for e in line]
        self.targettime = line

        self.greentarget = self.targettime 
        for i in range(self.greentime):
            temp1 = [e+i for e in self.targettime]
            temp2 = [max(e-i,0) for e in self.targettime]
            self.greentarget += temp1 + temp2
            self.greentarget = list(set(self.greentarget))

        tbelow = [e - self.greentime for e in self.targettime]
        tabove = [e + self.greentime for e in self.targettime]
        temp1 = []
        temp2 = []
        for i in range(self.yellowtime):
            temp1 += [max(e - i,0) for e in tbelow] 
            temp2 += [e + i for e in tabove] 
        self.yellowtarget = temp1 + temp2
        self.yellowtarget = list(set(self.yellowtarget)) 
        self.yellowtarget = [e for e in self.yellowtarget if e not in self.greentarget]


class Tracker(QLabel):
    newPoint = pyqtSignal(QPoint)
    clickPoint = pyqtSignal(QPoint)
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.path = QPainterPath()    
        self.setMouseTracking(True)
        self.position=0

        self.targettime = parent.targettime

        self.greentarget = parent.greentarget
        self.yellowtarget = parent.yellowtarget

        self.white = QPixmap('White.png')
        self.green = QPixmap('Green.png')
        self.yellow = QPixmap('Yellow.png')
        self.setPixmap(self.white)
        parent.pevent.connect(self._update)

    def _update(self, position):
        self.position = position
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if int(self.position) in self.greentarget:
            painter.drawPixmap(self.rect(), self.green)
        elif int(self.position) in self.yellowtarget:
            painter.drawPixmap(self.rect(), self.yellow)
        else:
            painter.drawPixmap(self.rect(), self.white)

    def mousePressEvent(self, event):
        self.clickPoint.emit(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        self.path.moveTo(event.pos())
        self.newPoint.emit(event.pos())
        self.update()

    def sizeHint(self):
        return QSize(400, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow(sys.argv[1], sys.argv[2], sys.argv[3])
    player.resize(1800, 480)        
    player.show()
    sys.exit(app.exec_())
