#include "udpserver.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    UDPServer w;
    w.show();
    w.setStyleSheet("background-image:url(:images/circuitry.png)");
//    w.repaint(); w.update();
    return a.exec();
}
