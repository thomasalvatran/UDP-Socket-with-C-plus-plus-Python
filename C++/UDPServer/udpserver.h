#ifndef UDPSERVER_H
#define UDPSERVER_H

//#include <QDialog>
//#include <QObject>
//#include <QUdpSocket>
//#include <QDebug>
//#include "udpserver.h"
#include <QDialog>
#include <QTimer>
#include <QUdpSocket>
#include <QMessageBox>
#include "GPIOClass.h"


namespace Ui {
class UDPServer;
}

class UDPServer : public QDialog
{
    Q_OBJECT

public:
    explicit UDPServer(QWidget *parent = 0);
    ~UDPServer();
    void WriteData( const QString& );
    void on();
    void off();

public slots:
    void readReady();
    void on_TOGGLE_stateChanged(int arg1);
    void on_TOGGLE_clicked();
    void SayHello();
    void on_EXIT_clicked();

private slots:
    void on_HELLO_clicked();

    void on_ON_clicked();

private:
    GPIOClass *gpio4;
    QUdpSocket socketServer;
    Ui::UDPServer *ui;
    QTimer timer;
};

#endif // UDPSERVER_H
