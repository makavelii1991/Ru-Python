import os
import time
import shutil

class ls:
    #Функция вывода списка файлов в директории
    def listdir():
        print(os.listdir())

class dir:
    #Создание новой директории
    def mkdir(name):
        try:
            os.mkdir(name)
        except FileExistsError:
            print("Такая папка уже существует.")
    #Удаление директории
    def rmdir(name):
        try:
            os.rmdir(name)
        except FileNotFoundError:
            print("Такой папки не существует.")
        except OSError:
            del_file = print(input("Папка содержит файлы. Чтобы продолжить удаление нажмите - 1: "))
            if del_file != 1:
                shutil.rmtree(name)
                print(name, "была удалена.")
            else:
                print(name, "не была удалена.")

class file:
    #Создать/перезаписать файл
    def add(name):
        if name in os.listdir():
            try:
                rewrite_question = input("Файл содержит данные. Если хотите его перезаписать, нажмите - 1: ")
                if rewrite_question == "1":
                    print("Введите текст документа:")
                    with open(name, 'w') as f:
                        f.write(input())
                        print("Файл", name, "изменен.")
                else:
                    print("Файл", name, "не был изменен. ")
            except PermissionError:
                print("Ошибка доступа")

        else:
            print("Введите текст документа:")
            with open(name, 'w') as f:
                f.write(input())
                print("Файл", name, "успешно создан, и введенный текст был сохранен.")
    #Открыть файл на чтение
    def read(name):
        try:
            with open(name) as f:
                print(f.read())
        except FileNotFoundError:
            print("Такого файла не существует")
        except PermissionError:
            print("Ошибка доступа")
    #Удаление файлов
    def rm(name):
        try:
            os.remove(name)
            print(name, "был удален")
        except FileNotFoundError:
            print(name, "уже существует")
        except PermissionError:
            print(name, "удалить невозможно.")
    #Информация о файле
    def info(name):
        try:
            file_info = os.stat(name)
            print(file_info.st_mode, " - бит защиты")
            print(file_info.st_ino, " - номер inode")
            print(file_info.st_dev, " - устройство")
            print(file_info.st_nlink, " - количество жестких ссылок")
            print(file_info.st_uid, " - идентификатор пользователя")
            print(file_info.st_gid, " - идентификатор группы пользователя")
            print(file_info.st_size, " - размер файла, в байтах")
            print(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_atime)), " - время последнего доступа")
            print(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_mtime)), " - время последнего изменения файла")
            print(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_ctime)), " - время создания файла")
        except FileNotFoundError:
            print(name, "не существует.")
