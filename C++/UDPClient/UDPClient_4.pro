#-------------------------------------------------
#
# Project created by QtCreator 2017-04-19T11:46:49
#
#-------------------------------------------------

QT       += core gui network designer

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = UDPClient_4
TEMPLATE = app


SOURCES += main.cpp\
        udpclient.cpp \
    formdialog.cpp \
#    iconeditorplugin.cpp

HEADERS  += udpclient.h \
    formdialog.h \
#    iconeditorplugin.h

FORMS    += udpclient.ui \
    formdialog.ui


RESOURCES += \
    images.qrc

IMAGES += images/ON.png images/OFF.png

QMAKE_CXX = g++-4.9
QMAKE_CXXFLAGS += -std=c++11

#no need it is install [QT_INSTALL_PLUGINS] Qt book
#INCLUDEPATH += /home/tovantran/TestQt/qt-book/chap05/iconeditorplugin
#LIBS += -L"/home/tovantran/TestQt/qt-book/chap05/iconeditorplugin" -liconeditorplugin
