import sys
import sqlite3
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()

    def load_data(self):
        db = sqlite3.connect('coffee.sqlite')
        db.cursor()
        request = db.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(request))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'variety', 'roasting', 'type',
                                                    'description', 'price', 'volume'])
        for i, row in enumerate(request):
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    form = Coffee()
    form.show()
    sys.exit(app.exec())
