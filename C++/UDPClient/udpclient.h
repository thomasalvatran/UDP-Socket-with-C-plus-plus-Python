#ifndef UDPCLIENT_H
#define UDPCLIENT_H

#include <QDialog>
#include <QTimer>
#include "udpclient.h"
#include <QObject>
#include <QUdpSocket>
#include <QWhatsThis>



namespace Ui {
class UDPClient;
}

class UDPClient : public QDialog
{
    Q_OBJECT

public:
    explicit UDPClient(QWidget *parent = 0);
    ~UDPClient();
    unsigned int ON_state;
    void WriteData( const QString& );


public slots:
    void readReady();
    void SayHello();
    void updateUDPClient(const QHostAddress&, quint16);
    void readReady_1();
    QString whatsThis() const;

signals:

private slots:

    void on_ON_clicked();
    void on_TOGGLE_stateChanged(int arg1);
    void on_TOGGLE_clicked();
    void on();
    void off();
    void on_EXIT_clicked();
    void led (const QString&);
    void ledON_clicked();
    void ledOFF_clicked();
    void changeIP_clicked();
    void changePort_clicked();

private:
    Ui::UDPClient *ui;
    UDPClient *udpclientON; //object
    UDPClient *udpclientOFF;
    QTimer timer;
    QUdpSocket clientSocket;
    QUdpSocket clientSocket_1;
};

#endif // UDPCLIENT_H
