# -*- coding: utf-8 -*-
import os
import time
import shutil
import socket

adr = u"C:/Users/йцу/Desktop/forGit Project/"

def ls():
    '''Сортировка и вывод по спискам: файлы, папки'''
    list_all_dirs = []
    list_all_files = []
    names = os.listdir(adr)
    for name in names:
        fullname = os.path.join(adr, name) # получаем полное имя
        if os.path.isfile(fullname):
            list_all_files.append(name)
        elif os.path.isdir(fullname):
            list_all_dirs.append(name)

    conn.send(("--------------------------------------------------\n").encode("cp866"))
    conn.send(("Папки: " + "\n" + str(list_all_dirs) + "\n").encode("cp866"))
    conn.send(("--------------------------------------------------\n").encode("cp866"))
    conn.send(("Файлы: " + "\n" + str(list_all_files) + "\n").encode("cp866"))
    conn.send(("--------------------------------------------------\n").encode("cp866"))
def mkdir_func():
    '''Создание новой папки'''
    try:
        conn.send(("Введите название папки: ").encode("cp866"))
        mkdir_name = conn.recv(1024).decode("cp866").strip()
        os.mkdir(str(adr + mkdir_name))
        conn.send(("Папка создана." + "\n").encode("cp866"))
    except FileExistsError:
        conn.send(("Файл/папка с таким именем уже существует."  + "\n").encode("cp866"))
def rmdir_func():
    '''Удаление папки'''
    try:
        conn.send(("Введите название папки: ").encode("cp866"))
        rmdir_name = conn.recv(1024).decode("cp866").strip()
        os.rmdir(str(adr + rmdir_name))
        conn.send(("Папка удалена." + "\n").encode("cp866"))
    except FileNotFoundError:
        conn.send(("Такая папка не существует." + "\n").encode("cp866"))
    except NotADirectoryError:
        conn.send(("Такая папка не существует." + "\n").encode("cp866"))
    except OSError:
        shutil.rmtree(adr + message.text)
        conn.send(("Папка удалена." + "\n").encode("cp866"))
def add():
    '''Создание и/или изменение файла'''
    conn.send(("Введите название файла: ").encode("cp866"))
    file_name = str(conn.recv(1024).decode("cp866").strip())
    name = str(adr + file_name)

    if file_name in os.listdir(adr):
        if os.path.getsize(name) != 0:
            conn.send(("Если хотите перезаписать введите - 1, и нажмите Enter." + "\n").encode("cp866"))
            askNum = conn.recv(1024).decode("cp866").strip()

            if askNum == "1": askTex(name)
            else: conn.send('==> ').encode("cp866")

        else: askTex(name)
    else: askTex(name)
def read():
    '''Чтение файла'''
    try:
        conn.send(("Введите название файла: ").encode("cp866"))
        read_name = conn.recv(1024).decode("cp866").strip()
        name = str(adr + read_name)
        with open(name, "r", encoding="utf-8") as f:
            conn.send((f.read() + "\n").encode("cp866"))
    except FileNotFoundError:
        conn.send(("Такого файла не существует." + "\n").encode("cp866"))
    except PermissionError:
        conn.send(("Ошибка доступа." + "\n").encode("cp866"))
def rm_file():
    '''Удаление файла'''
    try:
        conn.send(("Введите название файла: ").encode("cp866"))
        rm_name = conn.recv(1024).decode("cp866").strip()
        os.remove(str(adr + rm_name))
        conn.send(("Файл удален." + "\n").encode("cp866"))
    except FileNotFoundError:
        conn.send(("Данного файла не существует." + "\n").encode("cp866"))
    except PermissionError:
        conn.send(("Выбранный объект не является файлом. Удаление невозможно." + "\n").encode("cp866"))
def info():
    '''Информация о файле/папке'''
    try:
        conn.send(("Введите название файла: ").encode("cp866"))
        info_name = conn.recv(1024).decode().strip()
        name = str(adr + info_name)
        file_info = os.stat(name)
        conn.send(("---------------------------------------\n").encode("cp866"))
        conn.send((str(file_info.st_mode) + " - бит защиты \n").encode("cp866"))
        conn.send((str(file_info.st_ino) + " - номер inode \n").encode("cp866"))
        conn.send((str(file_info.st_dev) + " - устройство \n").encode("cp866"))
        conn.send((str(file_info.st_nlink) + " - количество жестких ссылок \n").encode("cp866"))
        conn.send((str(file_info.st_uid) + " - идентификатор пользователя \n").encode("cp866"))
        conn.send((str(file_info.st_gid) + " - идентификатор группы пользователя \n").encode("cp866"))
        conn.send((str(file_info.st_size) + " - размер файла, в байтах \n").encode("cp866"))
        conn.send((str(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_atime))) + " - время последнего доступа \n").encode("cp866"))
        conn.send((str(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_mtime))) + " - время последнего изменения файла \n").encode("cp866"))
        conn.send((str(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_ctime))) + " - время создания файла \n").encode("cp866"))
        conn.send(("---------------------------------------\n").encode("cp866"))
    except FileNotFoundError:
        conn.send(("Такого файла не существует." + "\n").encode("cp866"))
def askTex(name):
    conn.send(('Введите текст: ').encode("cp866"))
    askText = conn.recv(1024).decode("cp866").strip()
    try:
        with open(name, 'w',  encoding="utf-8") as f:
            f.write(askText)
        conn.send(('Текст сохранен.' + "\n").encode("cp866"))
    except PermissionError:
        conn.send(("Ошибка доступа." + "\n").encode("cp866"))

#Создание подключения, и вывод меню со справкой.
sock = socket.socket()
sock.bind(('localhost', 3333))
sock.listen(3)
conn, addr = sock.accept()
print( 'Connected:', addr)

hello = ("Добро пожаловать в Файловый менеджер для сервера." + "\n"
        "Воспользуйся командой: help, чтобы узнать перечень доступных команд." + "\n")
conn.send(hello.encode("cp866"))

while True:
    commands_bi = conn.recv(1024)
    if not commands_bi:
        break
    name = commands_bi.decode("cp866").strip()

    if name == 'mkdir': mkdir_func()
    elif name == 'rmdir': rmdir_func()
    elif name == 'rm': rm_file()
    elif name == 'read': read()
    elif name == 'info': info()
    elif name == "ls": ls()
    elif name == "add": add()
    elif name == "help":
        conn.send(( "---------------------------------" + "\n" +
                    "Список файлов---------------ls"  + "\n" +
                    "Создать новую папку---------mkdir" + "\n" +
                    "Удалить папку---------------rmdir"  + "\n" +
                    "Создать или Изменить файл---add" + "\n" +
                    "Прочитать файл--------------read"  + "\n" +
                    "Удалить файл----------------rm"  + "\n" +
                    "Информация о файле----------info"  + "\n"
                    "---------------------------------" + "\n"
                    ).encode("cp866"))

conn.close()
