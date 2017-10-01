#include "udpclient.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    UDPClient w;
    w.show();
    w.WriteData("Hello to Server");
    return a.exec();
}
