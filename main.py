import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from UI import Ui_MainWindow
from addEditCoffeeForm import Ui_dialog


class Coffee_db(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.db_filename = 'data/coffee.sqlite'
        self.db_rows = 0
        self.result = []
        self.setupUi(self)
        self.open_db()
        self.pushButton_add.clicked.connect(self.add_record)
        self.pushButton_change.clicked.connect(self.modify_record)
        self.pushButton_delete.clicked.connect(self.delete_record)

    def open_db(self):
        self.con = sqlite3.connect(self.db_filename)
        self.cur = self.con.cursor()
        self.result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.db_rows = len(self.result)
        self.load_table(self.result)
        self.con.commit()

    def load_table(self, res):
        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def add_record(self):
        self.record = Rec(self)
        self.record.label_10.setText('Добавить новую запись')
        self.record.exec()
        new_rec = self.record.return_record()
        if (new_rec[0]) != '':
            self.cur.execute("""INSERT INTO coffee(sort, roasting, ground_grain, taste,
                                price, volume) VALUES (?, ?, ?, ?, ?, ?)""", new_rec)
            QMessageBox.about(self, 'Сообщение', 'Запись добавлена')
        self.result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.con.commit()
        self.db_rows = len(self.result)
        self.load_table(self.result)

    def modify_record(self):
        if len(self.tableWidget.selectedItems()) > 0:
            row = [i.row() for i in self.tableWidget.selectedItems()][0]
            if row == self.db_rows:
                return
        else:
            return
        row_data = []
        for j in range(7):
            item = self.tableWidget.item(row, j)
            item_text = item.text() if item is not None else ''
            row_data.append(item_text)
        mod_choose = QMessageBox.question(self, "Внимание", "Запись\n"
                                          + row_data[0] + ' ' + row_data[1] + ' '
                                          + "\nбудет изменена",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if mod_choose == QMessageBox.No:
            return
        self.record = Rec(self)
        self.record.label_10.setText('Изменить запись')
        self.record.fill_record(row_data)
        self.record.exec()
        mod_rec = self.record.return_record()
        if mod_rec != ():
            self.cur.execute("""DELETE FROM coffee WHERE ID = ? AND
                                sort = ?""",
                             (row_data[0], row_data[1]))
            if mod_rec[0] != '':
                self.result = self.cur.execute("SELECT * FROM coffee").fetchall()
                self.cur.execute("INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (int(row_data[0]),) + mod_rec)
                QMessageBox.about(self, 'Сообщение', 'Запись изменена')
        self.result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.con.commit()
        self.db_rows = len(self.result)
        self.load_table(self.result)

    def delete_record(self):
        if len(self.tableWidget.selectedItems()) > 0:
            row = [i.row() for i in self.tableWidget.selectedItems()][0]
        else:
            return
        full_name = (self.tableWidget.item(row, 0).text(),
                     self.tableWidget.item(row, 1).text())
        mod_choose = QMessageBox.question(self, "Внимание", "Запись\n"
                                          + full_name[0] + ' ' + full_name[1] + ' '
                                          + "\nбудет удалена",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if mod_choose == QMessageBox.No:
            return
        if full_name != ('', ''):
            self.cur.execute("""DELETE FROM coffee WHERE ID = ? AND
                                sort = ?""", full_name)
            self.con.commit()
        self.result = self.cur.execute("SELECT * FROM coffee").fetchall()
        self.db_rows = len(self.result)
        self.load_table(self.result)
        QMessageBox.about(self, 'Сообщение', 'Запись удалена')


class Rec(QDialog, Ui_dialog):
    def __init__(self, Coff):
        super().__init__()
        self.setupUi(self)
        self.rec = ()

    def return_record(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        return self.rec

    def accept(self):
        if self.lineEdit.text() != '':
            record = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
                      self.lineEdit_4.text()]
            if self.lineEdit_5.text() != '':
                record.append(int(self.lineEdit_5.text()))
            else:
                record.append('')
            if self.lineEdit_6.text() != '':
                record.append(int(self.lineEdit_6.text()))
            else:
                record.append('')
            self.rec = tuple(record)
            self.close()

    def fill_record(self, row):
        self.lineEdit.setText(row[1])
        self.lineEdit_2.setText(row[2])
        self.lineEdit_3.setText(row[3])
        self.lineEdit_4.setText(row[4])
        self.lineEdit_5.setText(row[5])
        self.lineEdit_6.setText(row[6])


app = QApplication(sys.argv)
ex = Coffee_db()
ex.show()
sys.exit(app.exec_())
