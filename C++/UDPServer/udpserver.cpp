#include "udpserver.h"
#include "ui_udpserver.h"


QHostAddress senderClient; //store IP and port from UDPClient
quint16 portClient;
int helloCount = 0;

UDPServer::UDPServer(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::UDPServer)
{
    ui->setupUi(this);

    gpio4 = new GPIOClass("4"); //create new GPIO object to be attached to  GPIO4
    gpio4->export_gpio(); //export GPIO4
    gpio4->setdir_gpio("out"); // GPIO17 set to input

    socketServer.bind(QHostAddress::Any,9999 );
   //  socketServer.bind(QHostAddress("192.168.1.140"),9999 );
    connect(&socketServer, SIGNAL(readyRead()), this, SLOT(readReady()));
    connect(&timer, SIGNAL(timeout()), this, SLOT(on_TOGGLE_clicked()));
    timer.start(5000);
//    connect(ui->HELLO, SIGNAL(clicked()), this, SLOT(on_HELLO_clicked()));
    connect(ui->HELLO, SIGNAL(clicked()), this, SLOT(SayHello()));

    ui->display_message_to->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_port_to->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_data_to->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_message_from->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_port_from->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_data_from->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");

    setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint); //make widget pop up center
}

void UDPServer::readReady()
{
    qDebug() << "readReady";
    QByteArray buffer;
    buffer.resize(socketServer.pendingDatagramSize());

    QHostAddress sender;
    quint16 port;
    socketServer.readDatagram(buffer.data(),buffer.size(),&sender,&port);
    qDebug()<< "Server IP Responded" << sender.toString();
    qDebug()<< "Server Port Number" << port;
    qDebug()<< "Data "<< buffer;
    QString str = QString(buffer);
    ui->display_message_from->setText(QString(sender.toString()));
    ui->display_port_from->setText(QString::number(port));
    ui->display_data_from->setText(QString(str));
    str = str.trimmed(); //remove \n \cr
    QString match = QString("ON");
    qWarning() <<  "====================" << str.contains(match);
    if (str.contains(match))
    {
        on();
        gpio4->setval_gpio("1");
        buffer.append(" -> TURN GPIO ON");
    }
    else
    {
        off();
        gpio4->setval_gpio("0");
        buffer.append(" -> TURN GPIO");
    }
    ui->display_message_to->setText(QString(sender.toString()));
    ui->display_port_to->setText(QString::number(port));
    ui->display_data_to->setText(QString(buffer));
    socketServer.writeDatagram( buffer, sender, port );  //send back the same port and same address
    senderClient = sender;
    portClient = port;

    ui->display_message_from->update(); //why need update setText is enough
    ui->display_port_from->update();
    ui->display_data_from->update();
    ui->display_message_to->update();
    ui->display_port_to->update();
    ui->display_data_to->update();

}

void UDPServer::WriteData(const QString& data)
{
    QByteArray serverData;
    serverData.append( data);
    // write to the port, listening by the server.
    qDebug()<<"Writing datagram to 9999 port";
    socketServer.writeDatagram(serverData, QHostAddress::LocalHost, 9999 );

}

void UDPServer::SayHello()
{
    QByteArray Data;
    helloCount++;
    Data.append("Hello client "+ QString::number(helloCount));
    ui->display_message_to->setText(QString(senderClient.toString()));
    ui->display_port_to->setText(QString::number(portClient));
    ui->display_data_to->setText(QString(Data));
    ui->display_message_to->update();
    ui->display_port_to->update();
    ui->display_data_to->update();
    socketServer.writeDatagram(Data, QHostAddress(senderClient), portClient);
    qDebug() << "SayHello() " << helloCount;
    socketServer.flush();
}

void UDPServer::on()  //WON'T WORK IN THE LOOP use timer
{
    qDebug() << "on()";
    QPixmap ledon(":images/LEDON.png");
    QIcon icon1(ledon);
    ui->LED->setIcon(icon1);
    ui->LED->setIconSize(QSize(124, 305));
}

void UDPServer::off()
{
    qDebug() << "off()";
    QPixmap ledoff(":images/LEDOFF.png");
    QIcon icon3(ledoff);
    ui->LED->setIcon(icon3);
    ui->LED->setIconSize(QSize(124, 305));
}

void UDPServer::on_EXIT_clicked()
{
    //ui->EXIT->close();
    QMessageBox msgBox;
    int ret = QMessageBox::information(this, tr(""),
                                   tr("<font color = red >Are you sure you want to quit?.\n"
                                      "Shut Down key is pressed </font >"),
                                   QMessageBox::Ok | QMessageBox::Cancel);

    msgBox.setStyleSheet(QString::fromUtf8("background-color: rgb(241, 241, 241);"));
    switch (ret) {
    case QMessageBox::Ok :
        qApp->quit();
        break;

    case QMessageBox::Cancel :
        break;

    default :
        break;
    }
}

UDPServer::~UDPServer()
{
    delete ui;
}

void UDPServer::on_TOGGLE_clicked()
{

    qDebug() << "on_TOGGLE_clicked 3";
    if (ui->TOGGLE->isChecked())           //toggle is set going start timer
    {
        timer.start(1000);
//        on_HELLO_clicked();
        SayHello();
    }
    else
        timer.stop();
}

void UDPServer::on_TOGGLE_stateChanged(int arg1)
{
    qDebug() << "Toggle on stateChanged 2"; //method1
    if (arg1)
        qDebug() << "Checkbox is Checked";
    else
        qDebug() << "Checkbox is Unchecked";

    if (ui->TOGGLE->isChecked())
        QMessageBox::information(this, "Toogle", "Toggle in 1 second");
}


//Remember that connections are not between classes, but between instances (object).
//If you emit a signal and expect connected slots to be called, it must be
//emitted on an instance on which the connection was made.
