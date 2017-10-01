#ifndef FORMDIALOG_H
#define FORMDIALOG_H

#include <QDialog>
#include <QHostAddress>

namespace Ui {
class FormDialog;
}

class FormDialog : public QDialog
{
    Q_OBJECT

public:
    explicit FormDialog(QWidget *parent = 0);
    ~FormDialog();
    QString whatsThis() const;

public slots:
    void buttonBox_OK();
//    void update(); if override update of QObject

private slots:


    void buttonBox_Cancel();

signals:
    void updateParent(const QHostAddress&, quint16);  // no need to defined it just a signal emit to parent to receive it

private:
    Ui::FormDialog *ui;
};

#endif // FORMDIALOG_H
