import sys  # sys нужен для передачи argv в QApplication
import db_manager
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from PyQt5.QtWidgets import QMessageBox


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow): # взаимодействие с пользователем
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.update_list()
        self.pushButton_3.clicked.connect(self.verify)

    def update_list(self):
        self.listWidget.clear()
        global unverified
        unverified= []
        self.listWidget.addItem("Выберите документ:")
        list = db_manager.get_docs(True)
        for i in list.each():
            tmp_obj= i.val()
            if(tmp_obj['approved:']==False):

                 unverified.append(i)
                 self.listWidget.addItem(tmp_obj['name'])

    def verify(self):
        #тут я получаю значение с флешки для сравнения
        global unverified
        current_item = self.listWidget.currentRow()
        if current_item == 0:
            return

        current_item-=1
        f = open('E:\storage.txt', 'r+')
        encrypted = f.readline()
        f.close()
        result = ""
        for i in range(len(encrypted)):
            num = ord(encrypted[i]) - 16
            result += chr(num)
        checked = db_manager.get_user_with_sign(result)
        msg = QMessageBox()
        msg.setWindowTitle("Результат")
        if checked==None:
            msg.setText("Ошибка подпись не совпадаает с подписью в базе.")
            msg.exec_()
            print("Ошибка подпись не совпадаает с подписью в базе.")
            self.update_list()
            return
        if unverified[current_item].val()['level_required:'] < checked.val()['level']:
            msg.setText("Ошибка недостаточные привелегии.")
            msg.exec_()
            print("Ошибка недостаточный привелегии.")
            self.update_list()
            return
        if checked.key() in unverified[current_item].val()['users_signed'].keys():
            msg.setText("Вы уже подписывали данный документ.")
            msg.exec_()
            print("Вы уже подписывали данный документ.")
            self.update_list()
            return
        doc_id = unverified[current_item].key()
        db_manager.success(doc_id,checked.key())
        msg.setText("Вы успешно подписали документ")
        msg.exec_()
        print("Верификация успешно пройдена.")
        self.update_list()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()