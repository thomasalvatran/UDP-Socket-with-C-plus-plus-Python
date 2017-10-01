#-------------------------------------------------
#
# Project created by QtCreator 2017-04-23T03:55:29
#
#-------------------------------------------------

QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = UDPServer_6
TEMPLATE = app


SOURCES += main.cpp\
        udpserver.cpp \
    GPIOClass.cpp

HEADERS  += udpserver.h \
    GPIOClass.h

FORMS    += udpserver.ui

RESOURCES += \
    images.qrc
