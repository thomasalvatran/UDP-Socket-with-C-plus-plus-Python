#!/usr/bin/python

import sys
import socket, time
from PyQt4 import QtGui, QtCore
from PyQt4 import QtCore as qtcore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

global ex

global UDP_IP, UDP_PORT
UDP_IP = "192.168.2.114"
UDP_PORT = 9999

MESSAGE = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP
                 

def centerOnScreen(widget):
    desktopWidget = QApplication.desktop()
    screenRect = desktopWidget.availableGeometry(widget)
    widget.move(screenRect.center() - widget.rect().center())

class ExtendedQLabel(QtGui.QLabel):
    def __init(self, parent):
        QLabel.__init__(self, parent)
        print ("ctor")

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked()'))

class MyThreadRun(QThread):
    updateSignal = pyqtSignal(int)

    def __init__(self):
        super(MyThreadRun, self).__init__()
        global sock
        # threading.Thread.__init__(self)

        HOST = ''    # Symbolic name meaning all available interfaces
        PORT = 9999  # Arbitrary non-privileged port

        print("Thread...Run00")

    def run(self):

        while True:
            global sock
            print("Thread...Run")

            d = sock.recvfrom(1024)  # wait here until receive data
            data = d[0]
            addr = d[1]

            print ("data === " + str(data))

            if not data:
                break

            reply = 'Rx...' + data
            if (data.strip().find('ON') != -1):
                self.updateSignal.emit(1)
            else:
                self.updateSignal.emit(0)
            print ('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip())
            ex.st = str(addr[0]) + "<br>" + str(addr[1]) + "<br>" + str(data)
            ex.txt1_1.setText(ex.st)
            print ('-- addr ---- ' + str(addr))

class FormChange(QtGui.QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, foc):
        super(FormChange, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)
        self.setStyleSheet(" font-size:10pt;")
        self.line = QLineEdit(self)
        self.line.setText(str(UDP_IP))
        self.line1 = QLineEdit(self)
        self.line1.setText(str(UDP_PORT))
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel("IP address:"), self.line)
        layout.addRow(QtGui.QLabel("Port:"), self.line1)
        if foc == False:
            self.line.setFocus()
        else:
            self.line1.setFocus()
        self.submit = QPushButton("Submit")
        self.cancel = QPushButton("Cancel")
        layout.addRow(self.submit, self.cancel)
        self.submit.clicked.connect(self.ip_port)
        self.cancel.clicked.connect(self.close)
        self.setLayout(layout)
        self.setWindowTitle("IP Port")

    def ip_port(self):
        global UDP_IP, UDP_PORT
        print("ip_port")
        UDP_IP = self.line.text()
        print ("text: %s" % UDP_IP)
        print ("text: %s", UDP_IP)
        UDP_PORT = int(self.line1.text())
        print (UDP_PORT)
        ex.line.setText(str(UDP_IP))
        ex.line1.setText(str(UDP_PORT))
        self.close()

class MyLineEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def event(self, event):
        if (event.type() == QEvent.KeyPress) and (event.key() == Qt.Key_Return):
            self.emit(SIGNAL("returnPressed"))
            return True

        return QLineEdit.event(self, event)
class UDPClient(QDialog):

    def __init__(self):
        super(UDPClient, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) #remove what?this
        self.setModal(True)
        global toggle
        toggle = False
        self.worker = MyThreadRun()
        self.worker.updateSignal.connect(self.turnLED)
        self.resize(380, 270)
        self.move(200,200)
        self.setStyleSheet("QDialog { color:red;background-image:url(images/circuitry.png);}")

        o = QtGui.QLabel(self)
        o.setGeometry(0, 10, 400, 160)
        o.setStyleSheet("QLabel {background-color: rgba(233, 255, 255, 85%);}")

        self.pic = QtGui.QLabel(self)  #Qlabel
        self.pic.setGeometry(250, 40, 40, 80)
        self.pic.setPixmap(QtGui.QPixmap("images/LEDOFF.png").scaled(30, 85))

        self.pic1 = QtGui.QLabel(self)  # Qlabel
        self.pic1 = ExtendedQLabel(self)
        self.pic1.setGeometry(10, 170, 45, 45)
        self.pic1.setPixmap(QPixmap("images/OFF.png").scaled(45, 45,transformMode=QtCore.Qt.SmoothTransformation))
        self.pic1.connect(self.pic1, SIGNAL('clicked()'), self.buttonClicked)

        txt = QtGui.QLabel(self)
        txt.setGeometry(10, 10, 100, 20)
        txt.setText("Client")
        txt.setStyleSheet("QLabel { font-size:11pt;font-weight:bold;color:#FF0000; }")

        txt1 = QtGui.QLabel(self)
        txt1.setGeometry(10, 10, 200, 100)
        txt1.setText("Message to: <br> Port: <br> Data: <br>")

        self.txt1_1 = QtGui.QLabel(self)
        self.txt1_1.setStyleSheet("font-size:9pt;")
        self.txt1_1.setGeometry(85, 75, 200, 100)
        self.st = "0000" + "<br>" + "0000" + "<br>" + "00"
        self.txt1_1.setText(self.st)

        txt2 = QtGui.QLabel(self)
        txt2.setGeometry(10, 80, 100, 10)
        txt2.setText("Server")
        txt2.setStyleSheet("QLabel { font-size:11pt;font-weight:bold;color:#FF0000; }")

        txt2_1 = QtGui.QLabel(self)
        txt2_1.setGeometry(10, 80, 200, 100)
        txt2_1.setText("Message fr: <br> Port: <br> Data: <br>")

        self.txt2_2 = QtGui.QLabel(self)
        self.txt2_2.setStyleSheet("font-size:9pt;")
        self.txt2_2.setGeometry(85, 5, 200, 100)
        self.st = "0000" + "<br>" + "0000" + "<br>" + "00";
        self.txt2_2.setText(self.st)

        self.cb = QtGui.QCheckBox('Led Toggle', self)
        self.cb.setChecked(True)
        self.cb.setStyleSheet("font-size:10pt; font-weight:bold; background-color:white; color:#FF6600")
        self.cb.setToolTip('This will <b>Toggle LED 1 second on and off</b>')
        self.cb.move(250, 180)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.toggleLED)

        self.ip = QPushButton(self)
        self.port = QPushButton(self)
        self.ip.setText(" Change IP: ")
        self.port.setText("Change Port: ")
        self.ip.setToolTip("Change IP of UDP Server")
        self.port.setToolTip("Change Port of UDP Server")
        self.ip.resize(75, 20)
        self.port.resize(75, 20)

        self.ip.setStyleSheet("font-size:8pt")
        self.port.setStyleSheet("font-size:8pt")

        self.line = QLineEdit(self)
        self.line.setText(str(UDP_IP))
        self.line1 = QLineEdit(self)
        self.line1.setText(str(UDP_PORT))
        self.line.setStyleSheet("font-size:8pt")
        self.line1.setStyleSheet("font-size:8pt")
        # self.QLineEdit.setStyleSheet("font-size:8pt")
        self.line.resize(80, 18)
        self.line1.resize(40, 18)

        self.line.move(295, 132)
        self.line1.move(295, 155)
        self.ip.move(218, 130)
        self.port.move(218, 155)

        self.line.returnPressed.connect(self.lineedit_returnPressed)
        self.line1.returnPressed.connect(self.line1edit_returnPressed)
        self.ip.clicked.connect(lambda  : self.change(0))
        self.port.clicked.connect(lambda : self.change(1))
        self.setWindowTitle('UDP Client Connect First')
        self.show()

    def change(self, i):
        if i == 0:
            print ("Class change IP")
            self.w = FormChange(0)    #setfocus
        else:
            print ("Class change Port")
            self.w = FormChange(1)
        self.w.show()

    def lineedit_returnPressed(self):
        global UDP_IP
        UDP_IP = self.line.text()
        print ("text: %s" % UDP_IP)
        print ("text: %s", UDP_IP)

    def line1edit_returnPressed(self):
        global UDP_PORT
        UDP_PORT = int(self.line1.text())
        print (UDP_PORT)

    def gettext(self):
        print ("line...........")
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'UDP IP Server:')

        if ok:
            self.le1.setText(str(text))

    def toggleLED(self, state):
        print ("State of cb " + str(state))
        self.timer = QTimer()
        self.timer.timeout.connect(self.buttonClicked)
        if state == False:     # 1 is True 0 is false 2 is undefined
            self.timer.stop
        else:
            self.timer.start(1000)    # 1 second


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            # qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        else:
            event.ignore()

    def buttonClicked(self):
        print('Button Clicked')
        global toggle #, senddata, turnLED
        print(toggle)
        toggle ^= True
        if toggle == True:
            self.pic1.setPixmap(QPixmap("images/OFF.png").scaled(45, 45, transformMode=QtCore.Qt.SmoothTransformation))
            self.senddata("OFF")
        else:
            self.pic1.setPixmap(QPixmap("images/ON.png").scaled(45, 45, transformMode=QtCore.Qt.SmoothTransformation))
            self.senddata("ON")

    def receivedata(self, s):
        modifiedMessage, serverAddress = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:  ", modifiedMessage.decode('utf-8'))
        print("received message: %s " % modifiedMessage)
        if modifiedMessage.find('ON') != -1:
            self.pic.setPixmap(QtGui.QPixmap("images/LEDON.png").scaled(30, 85))
        else:
            self.pic.setPixmap(QtGui.QPixmap("images/LEDOFF.png").scaled(30, 85))

    def senddata(self, s):
        MESSAGE = s
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
        self.st = str(UDP_IP) + "<br>" + str(UDP_PORT) + "<br>" + str(s)
        self.txt2_2.setText(self.st)
        print("transmitted message Tx..." + MESSAGE)
    def turnLED(self, s):
        print('LED' + " --------- " + str(s))
        if s == 1:
            self.pic.setPixmap(QtGui.QPixmap("images/LEDON.png").scaled(30, 85))
        else:
            self.pic.setPixmap(QtGui.QPixmap("images/LEDOFF.png").scaled(30, 85))

    def startMyThreadRun(self):
        self.worker.start()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = UDPClient()
    centerOnScreen(ex)
    ex.startMyThreadRun()
    sys.exit(app.exec_())