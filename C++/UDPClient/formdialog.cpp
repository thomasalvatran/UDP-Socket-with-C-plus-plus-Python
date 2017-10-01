#include "formdialog.h"
#include "ui_formdialog.h"
#include <QDebug>
#include <QHostAddress>
#include <QDesignerCustomWidgetInterface>
#include <QWhatsThis>
#include "udpclient.h"

extern int UDP_PORT;
extern QHostAddress UDP_IP;


FormDialog::FormDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::FormDialog)
{
    ui->setupUi(this);
    ui->IP->setText(UDP_IP.toString());
    ui->Port->setText(QString::number(UDP_PORT));
    connect(ui->Ok,SIGNAL(accepted()),this, SLOT(buttonBox_OK()));
    connect(ui->Ok,SIGNAL(rejected()),this, SLOT(buttonBox_Cancel()));
    setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint); //make widget pop up center
    setModal(true);
}

FormDialog::~FormDialog()
{
    delete ui;
}

void FormDialog::buttonBox_OK()
{
    qDebug() << "Button 2 accepted";
    qDebug() << UDP_IP << " " << UDP_PORT;
    UDP_IP = QHostAddress(ui->IP->text()); //cast into QHostAddress
    UDP_PORT = ui->Port->text().toInt();

//Method 1
    emit updateParent(UDP_IP, UDP_PORT); //update is a part of Qt like PyQT also has update
//Method 2: crash with this or without this
//      ((UDPClient*)this->parentWidget())->updateUDPClient(UDP_IP, UDP_PORT); //don't forget this object

       UDPClient *w = dynamic_cast<UDPClient *>(this->parentWidget());
       if (0 != w)
           qDebug() << " OK ------------";    // NOT 0 has parent
       else
           qDebug() << " ERROR ------------NULL POINTER"; // 0 is has no parent

//       UDPClient::updateUDPClient(UDP_IP, UDP_PORT);        //cannot function without obj
//       this->UDPClient::updateUDPClient(UDP_IP, UDP_PORT);  //class FormDialog no updateUDPClient
      close();
}

void FormDialog::buttonBox_Cancel()
{
    qDebug() << "reject accepted";
    UDP_PORT = ui->Port->text().toInt();
    close();
}
