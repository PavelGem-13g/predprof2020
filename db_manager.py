#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pyrebase
import json

global db

config = {
    "apiKey": "AIzaSyCqqaW8DWQ3Gz_3jMJkx3x08_BgrjURpXk",
    "authDomain": "e-sign-d03fd.firebaseapp.com",
    "databaseURL": "https://e-sign-d03fd.firebaseio.com",
    "storageBucket": "e-sign-d03fd.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()
class User:  # пользватель (работник)
    def __init__(self, full_name, dob, deparment, position, e_sign, level):
        self.full_name = full_name
        self.dob = dob
        self.department = deparment
        self.position = position
        self.e_sign = e_sign
        self.level = level

def get_user_with_sign(signature): # получаем подпсь пользователя
     k =db.child("users").get()
     for i in k.each():
         if i.val()['e_sign']==signature:
             return i

def success(doc_id,user_id):  # если подписи совпадают создаем новую запись в бд
    was = db.child('docs').child(doc_id).child('valid_signed').get().val()
    new = was+1
    db.child('docs').child(doc_id).child('valid_signed').set(new)
    db.child('docs').child(doc_id).child('users_signed').child(user_id).set(datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"))
    return

def new_user(): # создаем нового пользователя
    nuser = User(full_name=input("Введите полное имя сотрудника для регистрации:"),
                 dob=input("Введите дату рождения сотрудника:"),
                 deparment=input("Введите отдел, в котором числится сотрудник:"),
                 position=input("Введите должность сотрудника:"),
                 e_sign=input("Введите образец электронной подписи сотрудника:"),
                 level=input(
                     "Введите уровень доступа сотрудника 1-Ген. директор, 2-Зам начальник отдела, 3-Простой сотрудник:")
                 )
    print(nuser.__dict__)
    key = db.generate_key()
    print(key)
    db.child("users").child(key).set(nuser.__dict__)
    db.child("departments").child(nuser.department).push(key)

def get_docs(signed):
    return db.child('docs').get()

def new_doc(text,name,level):  # добавляем нового пользователя в бд
    key = db.generate_key()
    db.child("docs").child(key).child("name").set(name)
    db.child("docs").child(key).child("doc").set(text)
    db.child("docs").child(key).child("level_required:").set(level)
    db.child("docs").child(key).child("approved:").set(False)
    db.child("docs").child(key).child("valid_signed").set(0)
    db.child("docs").child(key).child("users_signed").set("")
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
#
# #jsonStr = json.dumps(nuser.__dict__)
# choice = int(input("выбреите, что хотите делать 1-зарегистрировать пользователя,2-создать новый документ для подписи: "))
#
# if choice==1:
#     new_user()
#
# if choice==2:
#     new_doc(input("Введите текст документа:"),input("Введите имя документа:"),input("Введите максимальный уровень доступа для подписи(1-Ген дир, 2-Зам нач., 3-все"))

