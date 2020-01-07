import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class Coffee_db(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_filename = 'coffee.sqlite'
        self.db_rows = 0
        self.result = []
        uic.loadUi('main.ui', self)
        self.open_db()

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


app = QApplication(sys.argv)
ex = Coffee_db()
ex.show()
sys.exit(app.exec_())
