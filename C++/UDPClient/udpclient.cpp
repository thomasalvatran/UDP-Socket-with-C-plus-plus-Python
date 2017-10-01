#include "formdialog.h"
#include "udpclient.h"
#include "ui_udpclient.h"
#include <QDebug>
#include <QToolButton>
#include <QMessageBox>
#include <QDesignerCustomWidgetInterface>
#include <QWidget>
//#include <QThread>

//QHostAddress UDP_IP = "192.168.2.114";
//QHostAddress UDP_IP;

QHostAddress UDP_IP("192.168.1.141");
quint16 UDP_PORT = 9999;

UDPClient::UDPClient(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::UDPClient)
{
    ui->setupUi(this);
    ON_state = 0;
    ui->TOGGLE->setChecked(false);
    connect( &timer, SIGNAL(timeout()), this, SLOT(on_TOGGLE_clicked()));
    timer.start(5000);
    connect(&clientSocket,SIGNAL(readyRead()),this,SLOT(readReady()));
    ui->display_message_to->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_port_to->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_data_to->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");


    ui->display_message_from->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_port_from->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    ui->display_data_from->setStyleSheet(" background: rgba(250, 250, 250, 0.4); font-size:12px; font-weight: bold; font-style: normal; margin:20px");
    setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint); //make widget pop up center
    ui->changeIP->setToolTip("Change IP of UDP Server");
    ui->changePort->setToolTip("Change Port of UDP Server");
    setStyleSheet("UDPClient {background-image: url(:/images/circuitry.png);}"); //set QDialog
    connect(ui->changeIP,SIGNAL(clicked()),this, SLOT(changeIP_clicked()));
    connect(ui->changePort,SIGNAL(clicked()),this, SLOT(changePort_clicked()));
    ui->IP->setText(UDP_IP.toString());
    ui->Port->setText(QString::number(UDP_PORT));
}

void UDPClient::updateUDPClient(const QHostAddress& s, quint16 i)
{
    qDebug() << " updateUDPClient " << s << " " << i;
    ui->IP->setText(s.toString());
    ui->Port->setText(QString::number(UDP_PORT));
}


void UDPClient::readReady_1()
{
    qDebug() << "readReady_1";
    QByteArray buffer;
    buffer.resize(clientSocket_1.pendingDatagramSize());
    QHostAddress sender;
    quint16 port;
    clientSocket_1.readDatagram(buffer.data(), buffer.size(), &sender, &port);
    qDebug()<< "Server IP Responded" << sender.toString();
    qDebug()<< "Server Port Number" << port;
    qDebug()<< "Size "<< buffer.size();
    qDebug()<< "Data "<< buffer;
    QString str = QString(buffer);
    ui->display_message_from->setText(QString(sender.toString()));
    ui->display_port_from->setText(QString::number(port));
    ui->display_data_from->setText(QString(str));
}

UDPClient::~UDPClient()
{
    delete ui;
}

void UDPClient::on_TOGGLE_clicked()
{

    qDebug() << "on_TOGGLE_clicked 3";
    if (ui->TOGGLE->isChecked())
    {
        timer.start(1000);
        on_ON_clicked();
    }
    else
        timer.stop();
}

void UDPClient::on_TOGGLE_stateChanged(int arg1)
{
    qDebug() << "Toggle on stateChanged 2"; //method1
    if (arg1)
        qDebug() << "Checkbox is Checked";
    else
        qDebug() << "Checkbox is Unchecked";

    if (ui->TOGGLE->isChecked())
        QMessageBox::information(this, "Toogle", "Toggle in 1 second");
}

void UDPClient::on()  //WON'T WORK IN THE LOOP use timer
{
    qDebug() << "on()";
    QPixmap on(":images/ON.png");
    QIcon icon(on);
    ui->ON->setIcon(icon);
    ui->ON->setIconSize(QSize(90, 90));

    QPixmap ledon(":images/LEDON.png");
    QIcon icon1(ledon);
    ui->LED->setIcon(icon1);
    ui->LED->setIconSize(QSize(124, 305));
}

void UDPClient::off()
{
    qDebug() << "off()";
    QPixmap off(":images/OFF.png");
    QIcon icon(off);               //icon place holder local variables
    ui->ON->setIcon(icon);
    ui->ON->setIconSize(QSize(90, 90));

    QPixmap ledoff(":images/LEDOFF.png");
    QIcon icon1(ledoff);
    ui->LED->setIcon(icon1);
    ui->LED->setIconSize(QSize(124, 305));
}

void UDPClient::on_ON_clicked()
{
    qDebug() << "-----------";
    ON_state ^= 1; //send to server then wait to receive msg to turn our LED
    if (ON_state == 1)
        //on();
        ledON_clicked();
    else
//        off();
        ledOFF_clicked();
}

void UDPClient::on_EXIT_clicked()
{
    //ui->EXIT->close();
    QMessageBox msgBox;
    int ret = QMessageBox::information(this, tr("Toggle"),
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

void UDPClient::WriteData(const QString& data)
{
    QByteArray clientData;
    clientData.append( data);
    clientSocket.writeDatagram(clientData, QHostAddress(UDP_IP.toString()), UDP_PORT );
}

void UDPClient::SayHello()
{
  qDebug() << "SayHello from udpclient";
}

void UDPClient::readReady()
{
    QByteArray buffer;
    buffer.resize(clientSocket.pendingDatagramSize());

    QHostAddress sender;
    quint16 port;
    clientSocket.readDatagram(buffer.data(),buffer.size(),&sender,&port);
    QString str = QString(buffer);
    ui->display_message_from->setText(QString(sender.toString()));
    ui->display_port_from->setText(QString::number(port));
    ui->display_data_from->setText(QString(str));
    str = str.trimmed(); //remove \n \cr
    QString match = QString("ON");
    if (str.contains(match))
    {
        on();
    }
    else
        off();
}

void UDPClient::ledON_clicked()   //should not have on_ledON but ledON will consume on_ledON and on_ start
{
    qDebug() << "ledON";
    led("ON");  //send
}

void UDPClient::ledOFF_clicked()
{
    qDebug() << "ledOFF";
    led("OFF");
}

void UDPClient::led(const QString& data)
{
    QByteArray d;
    d.append(data);
    clientSocket.writeDatagram(d, QHostAddress(UDP_IP.toString()), UDP_PORT );
    ui->display_message_to->setText(UDP_IP.toString());
    ui->display_port_to->setText(QString::number(UDP_PORT));
    ui->display_data_to->setText(QString(data));
    clientSocket.flush();
}

void UDPClient::changeIP_clicked()  //on_changeIP is using auto connect from GUI
{
    qDebug() << "button IP click 1";
    FormDialog *f = new FormDialog();  //focus is done in tab order
    connect(f, SIGNAL(updateParent(const QHostAddress&, quint16)), this, SLOT(updateUDPClient(const QHostAddress&, quint16)));
    f->show();
}

void UDPClient::changePort_clicked()
{
    qDebug() << "button IP click 1";
    FormDialog *f = new FormDialog();
    ui->Port->setFocus();
    ui->Port->update();
    f->show();
}

QString UDPClient::whatsThis() const
{
    qDebug() << "WhatsThis";
    return tr("This widget is presented in Chapter 5 of <i>C++ GUI "
    "Programming with Qt 4</i> as an example of a custom Qt "
    "widget.");
}
