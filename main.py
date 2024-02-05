import sys
import sqlite3
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class edit_form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        # self.saveBtn.clicked.connect(self.save_data)


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()
        self.edit_f = edit_form()
        self.edit_f.saveBtn.clicked.connect(self.save_data)
        self.edit_f.addBtn.clicked.connect(self.add_data)
        self.tableWidget.itemClicked.connect(self.edit)

    def edit(self, values):
        # получаем ID из строки по которой кликнули
        self.id_item = self.tableWidget.item(values.row(), 0).text()
        self.edit_f.setWindowTitle(f'Редактирование записи c id = {values.row()}')

        db = sqlite3.connect('coffee.sqlite')
        db.cursor()
        self.request2 = db.execute(f"""SELECT * FROM coffee WHERE id = {self.id_item}""").fetchall()
        # print(self.request2)
        self.edit_f.tableEdit.setColumnCount(7)  # количество столбцов
        self.edit_f.tableEdit.setRowCount(1)  # количество строк
        self.edit_f.tableEdit.setHorizontalHeaderLabels(['ID', 'variety', 'roasting', 'type',
                                                         'description', 'price', 'volume'])

        for j, col in enumerate(self.request2[0]):
            # print(j, col)
            self.edit_f.tableEdit.setItem(0, j, QTableWidgetItem(str(col)))

        self.edit_f.tableAdd.setColumnCount(6)
        self.edit_f.tableAdd.setRowCount(1)
        self.edit_f.tableAdd.setHorizontalHeaderLabels(['variety', 'roasting', 'type',
                                                        'description', 'price', 'volume'])
        self.edit_f.show()
        db.close()

    def load_data(self):
        db = sqlite3.connect('coffee.sqlite')
        db.cursor()
        self.request = db.execute(f"""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(self.request))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'variety', 'roasting', 'type',
                                                    'description', 'price', 'volume'])
        for i, row in enumerate(self.request):
            for j, col in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
        db.close()

    def save_data(self):
        db = sqlite3.connect('coffee.sqlite')
        db.cursor()
        self.request2 = db.execute(f"""UPDATE coffee SET 
                                    id = '{self.edit_f.tableEdit.item(0, 0).text()}',
                                    variety = '{self.edit_f.tableEdit.item(0, 1).text()}',
                                    roasting = '{self.edit_f.tableEdit.item(0, 2).text()}',
                                    type = '{self.edit_f.tableEdit.item(0, 3).text()}',
                                    description = '{self.edit_f.tableEdit.item(0, 4).text()}',
                                    price = '{self.edit_f.tableEdit.item(0, 5).text()}',
                                    volume = '{self.edit_f.tableEdit.item(0, 6).text()}'
                                    WHERE id = '{self.edit_f.tableEdit.item(0, 0).text()}'""")
        db.commit()

        db.close()
        self.load_data()
        self.edit_f.close()

    def add_data(self):
        db = sqlite3.connect('coffee.sqlite')
        db.cursor()
        db.execute(f"""INSERT INTO coffee('variety', 'roasting', 'type', 'description', 'price', 'volume')
                    VALUES (
                    '{self.edit_f.tableAdd.item(0, 0).text()}',
                    '{self.edit_f.tableAdd.item(0, 1).text()}',
                    '{self.edit_f.tableAdd.item(0, 2).text()}',
                    '{self.edit_f.tableAdd.item(0, 3).text()}',
                    '{self.edit_f.tableAdd.item(0, 4).text()}',
                    '{self.edit_f.tableAdd.item(0, 5).text()}')""")
        db.commit()
        db.close()
        self.load_data()
        self.edit_f.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    form = Coffee()
    form.show()
    sys.exit(app.exec())
