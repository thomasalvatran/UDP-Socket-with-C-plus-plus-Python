#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4 import QtCore as qtcore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import socket
import threading
import time


checkos = os.uname()
def setgpio(i):
    if checkos[1] == 'raspberrypi':
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
        GPIO.output(4, i)
    else:
        pass

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
        print("Thread...Run00")
        HOST = ''  # Symbolic name meaning all available interfaces
        PORT = 9999  # Arbitrary non-privileged port


        # Datagram (udp) socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print ('Socket created')
        # except socket.error, msg: #Python 2.7
        except socket.error as msg:  # Python 3.2
            print ('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        # Bind socket to local host and port
        try:
            sock.bind((HOST, PORT))
        except socket.error as msg:
            print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        print ('Socket bind complete')

        self.signal = qtcore.SIGNAL("signal")

    def run(self):

        while True:
            global sock
            print("Thread...Run")

            d = sock.recvfrom(1024)  #wait here until receive data
            data = d[0]
            addr = d[1]

            if not data:
                break

            reply = 'Rx...' + data
            if (data.strip().find('ON') != -1):
                setgpio(1)
                self.updateSignal.emit(1)

            else:
                self.updateSignal.emit(0)
                setgpio(0)

            sock.sendto(reply, addr)
            print ('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip())
            test_string = "Message receive from Client: " + reply
            print (test_string)

            ex.st = str(addr[0]) + "<br>" + str(addr[1]) + "<br>" + str(data)
            ex.st1 = str(addr[0]) + "<br>" + str(addr[1]) + "<br>" + str(reply)

            ex.txt1_1.setText(ex.st)
            ex.txt2_2.setText(ex.st1)
            ex.senderClient = str(addr[0])
            ex.portClient = str(addr[1])
            ex.toClient = addr
            print ('-- addr ---- ' + str(addr))

class MyThreadLoop(threading.Thread):
    # global sock, ex, txt3_1
    def run(self):
        cnt = 0

        while True:
            print("Thread...Loop")
            cnt += 1
            print("udp server running", cnt)
            test_string = "udb server running " + str(cnt)
            ex.changetxt3_1(test_string)  # similar get and set call function changetxt3_1
            time.sleep(10) # sleep at least 10 second for other thread to run thread is running
            # yield 1


class UDPServer(QDialog):
    # global ex, txt3_1
    def __init__(self):
        super(UDPServer, self).__init__()
        global toggle, helloCount
        toggle = False
        helloCount = 0
        self.worker = MyThreadRun()
        self.worker.updateSignal.connect(self.turnLED)
        senderClient = ' '
        portClient = ' '
        toClient = ' '
        self.resize(380, 270)
        self.move(200, 200)
        self.setStyleSheet("QDialog { color : red;background-image:url(images/circuitry.png);}")

        o = QtGui.QLabel(self)
        o.setGeometry(0, 10, 420, 180)
        o.setStyleSheet("QLabel {background-color: rgba(233, 255, 255, 85%);}")

        self.pic = QtGui.QLabel(self)  #Qlabel
        self.pic.setGeometry(250, 40, 40, 80)
        self.pic.setPixmap(QtGui.QPixmap("images/LEDOFF.png").scaled(30, 85))

        self.pic1 = ExtendedQLabel(self)
        self.pic1.setGeometry(10, 190, 70, 70)
        self.pic1.setPixmap(QtGui.QPixmap("images/say-hello.png").scaled(70, 70))
        self.pic1.connect(self.pic1, SIGNAL('clicked()'), self.helloClient) #signal and slot


        self.txt = QtGui.QLabel(self)
        self.txt.setGeometry(10, 10, 100, 20)
        self.txt.setText("Client")
        self.txt.setStyleSheet("QWidget { font-size:11pt;font-weight:bold;color:#FF0000; }")

        self.txt1 = QtGui.QLabel(self)
        self.txt1.setGeometry(10, 10, 100, 100)
        self.txt1.setText("Message to: <br> Port: <br> Data: <br>")

        self.txt1_1 = QtGui.QLabel(self)
        self.txt1_1.setGeometry(80, 70, 200, 100)
        self.st = "0000" + "<br>" + "0000" + "<br>" + "00";
        self.txt1_1.setText(self.st)

        self.txt2 = QtGui.QLabel(self)
        self.txt2.setGeometry(10, 80, 100, 10)
        self.txt2.setText("Server")
        self.txt2.setStyleSheet("QWidget { font-size:11pt;font-weight:bold;color:#FF0000; }")

        self.txt2_1 = QtGui.QLabel(self)
        self.txt2_1.setGeometry(10, 75, 100, 100)
        self.txt2_1.setText("Message fr: <br> Port: <br> Data: <br>")

        self.txt2_2 = QtGui.QLabel(self)
        self.txt2_2.setGeometry(80, 10, 200, 90)
        self.st1 = "0000" + "<br>" + "0000" + "<br>" + "00";
        self.txt2_2.setText(self.st1)

        self.txt3 = QtGui.QLabel(self)
        self.txt3.setGeometry(10, 150, 100, 10)
        self.txt3.setText("Server Status")
        self.txt3.setStyleSheet("QLabel { font-size:11pt;font-weight:bold;color:#FF0000; }")

        self.txt3_1 = QtGui.QLabel(self)
        self.txt3_1.setGeometry(10, 170, 150, 10)
        self.txt3_1.setText("UDP Server running:")

        cb = QtGui.QCheckBox('Hello Client', self)
        cb.setChecked(True)
        cb.setStyleSheet("QCheckBox { font-size:10pt; font-weight:bold; background-color:white; color:#FF6600}")
        cb.setToolTip('Enable will send <b>Hello to client every 1 second</b>')
        cb.move(250, 180)
        cb.toggle()
        cb.stateChanged.connect(self.hellomsg)
        self.setWindowTitle('UDP Server Socket')
        self.show()

    @property
    def x(self):
        """This method runs whenever you try to access self.x"""
        print("Getting self.x")
        return self._x

    @x.setter
    def x(self, value):
        """This method runs whenever you try to set self.x"""
        print("Setting self.x to %s" % (value,))
        self._x = value
    def changeTitle(self, state):
        if state == QtCore.Qt.Checked:
            self.setWindowTitle('QtGui.QCheckBox')
        else:
            self.setWindowTitle('UDP Client Socket')

    def changetxt3_1(self, st):
        self.txt3_1.setText(st)

    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def hellomsg(self, state):
        self.timer = QTimer()
        self.timer.timeout.connect(self.helloClient)
        if state == False:  # 1 is True 0 is false 2 is undefined
            self.timer.stop
        else:
            self.timer.start(1000)

    def helloClient(self):
        global helloCount
        print('Button Clicked' + " --------------- " + str(self.toClient))
        #addr = self.senderClient + self.portClient
        helloCount += 1

        s = "Hello to client %d" % helloCount
        s1 = "Hello " + str(helloCount)

        print ("------------------ " + s)
        sock.sendto(s, self.toClient)

        st1 = str(self.senderClient) + "<br>" + str(self.portClient) + "<br>" + str(s)
        self.txt2_2.setText(st1)
        print (st1)

    def turnLED(self, s):
        print('LED' + " --------- " + str(s))
        if s == 1:
            self.pic.setPixmap(QtGui.QPixmap("images/LEDON.png").scaled(30, 85))
        else:
            self.pic.setPixmap(QtGui.QPixmap("images/LEDOFF.png").scaled(30, 85))


    def appinit(self):
        tr = MyThreadRun()
        self.connect(thread, thread.signal, self.buttonClicked)
        # tr.start()

    def startMyThreadRun(self):
        self.worker.start()

if __name__ == '__main__':
    # main()
    app = QtGui.QApplication(sys.argv)
    ex = UDPServer()
    ex.show()

    ex.startMyThreadRun() #sstart thread from app so connect will wirk and emit from thread
    tl = MyThreadLoop()
    tl.start()
    sys.exit(app.exec_())

''' Note:

p. 128 of [Mark_Summerfield]_Rapid_GUI_Programming_with_Pyth.pdf
# Whenever a signal is emitted, by default PyQt simply throws it away! To take
# notice of a signal we must connect it to a slot. InC++/Qt, slots are methods that
# must be declared with a special syntax; but in PyQt, they can be any callable
# we like (e.g., any function or method), and no special syntax is required when
# defining them.

# ex.buttonClicked(data.strip()) #NOT WORKING WITH SetPixMap only text

# 1. self.worker.updateSignal.connect(self.buttonClicked)
# 2. self.updateSignal.emit(1)
# 3. ex.startMyThreadRun()  #START THREAD WITH EX(APP)


https://stackoverflow.com/questions/23718761/pyqt-signals-not-handled-in-qthread-but-in-main-thread
Your Worker objects 'live' in the main thread, that means all their signals will be handled by the main thread's event loop. '
'The fact that these objects are QThreads doesn't change that.
'''

