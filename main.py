import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("films_db.sqlite")
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.new_film)
        self.pushButton_3.clicked.connect(self.edit_films)
        self.setWindowTitle('Кофейня')
        self.select_data()

    def new_genres(self):
        self.genres = New_genres()
        self.genres.show()


    def edit_genres(self):
        self.verdict3 = self.tableWidget_2.currentRow()
        if self.verdict3 == -1:
            self.label_2.setText('Выберите строку')
        else:
            self.label_2.setText('')
            self.up_genre = Update_genre()
            self.up_genre.show()



    def new_film(self):
        self.films = New_film()
        self.films.show()

    def select_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        res = connection.cursor().execute("SELECT * FROM Coffee").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        title = ['ID', 'название сорта', 'степень обжарки',
                 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(res[i][j])))

    def closeEvent(self, event):
        self.connection.close()

    def edit_films(self):
        self.verdict2 = self.tableWidget.currentRow()
        if self.verdict2 == -1:
            self.label.setText('Выберите строку')
        else:
            self.label.setText('')
            self.up_film = Update_film()
            self.up_film.show()




class Update_film(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Изменить кофе')
        self.cur = self.con.cursor()
        uic.loadUi('addEditCoffeeForm.ui', self)
        result = self.cur.execute("""SELECT * FROM Coffee""").fetchall()[ex.verdict2]
        self.id_1 = result[0]
        self.pushButton.clicked.connect(self.add_films)

    def add_films(self):
        n1 = self.lineEdit.text()
        n2 = self.lineEdit_2.text()
        n3 = self.lineEdit_3.text()
        n4 = self.lineEdit_4.text()
        n5 = self.lineEdit_5.text()
        n6 = self.lineEdit_6.text()
        if '' in [n1, n2, n3, n4, n5, n6]:
            self.label_5.setText('Неверно заполнена форма')
        else:
            self.cur.execute(f'''UPDATE Coffee
            SET Name_sort = '{n1}'
            WHERE ID = {self.id_1}''')
            self.cur.execute(f'''UPDATE Coffee
            SET degree_of_roasting = '{n2}' 
            WHERE ID = {self.id_1}''')
            self.cur.execute(f'''UPDATE Coffee
            SET ground_in_grains = '{n3} '
            WHERE ID = {self.id_1}''')
            self.cur.execute(f'''UPDATE Coffee
            SET the_description_of_the_taste = '{n4} '
            WHERE ID = {self.id_1}''')
            self.cur.execute(f'''UPDATE Coffee
                        SET price = {n5} 
                        WHERE ID = {self.id_1}''')
            self.cur.execute(f'''UPDATE Coffee
                        SET the_volume_of_packaging = {n6} 
                        WHERE ID = {self.id_1}''')
            self.con.commit()
            ex.select_data()
            self.close()


class New_film(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Добавить кофе')
        self.pushButton.clicked.connect(self.add_films)

    def add_films(self):
        n1 = self.lineEdit.text()
        n2 = self.lineEdit_2.text()
        n3 = self.lineEdit_3.text()
        n4 = self.lineEdit_4.text()
        n5 = self.lineEdit_5.text()
        n6 = self.lineEdit_6.text()
        if '' in [n1, n2, n3, n4, n5, n6]:
            self.label_5.setText('Неверно заполнена форма')
        else:
            num = self.cur.execute(f'SELECT ID FROM Coffee').fetchall()
            if num == []:
                num = 1
            else:
                num = num[0][-1] + 1
            comand = f"""INSERT OR REPLACE INTO Coffee(ID, Name_sort, degree_of_roasting, ground_in_grains, the_description_of_the_taste, price, the_volume_of_packaging) VALUES ({num}, "{n1}", "{n2}", "{n3}", "{n4}", {n5}, {n6})"""
            self.cur.execute(comand)
            self.con.commit()
            ex.select_data()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())