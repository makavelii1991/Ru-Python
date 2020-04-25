import os
import time
import shutil
import telebot
from telebot import types


bot = telebot.TeleBot('1238053204:AAH4Pq_s6GizEXaBVI1_Y60U-Ud73_LJcKY') #Телеграм токен
adr = u"C:/Users/йцу/Desktop/forGit Project/03. FileManBot/cache/" #корень файлового менеджера
class dir:
    def mkdir(name):
        '''Создание новой директории'''
        os.mkdir(name)

    def rmdir(name):
        '''Удаление директории'''
        os.rmdir(name)
class ls:
    def listdir(name):
        '''Функция вывода списка файлов в директории'''
        return os.listdir(name)
class file:
    def rm(name):
        os.remove(name)
def list_all():
    '''Сортировка по спискам: файлы, папки'''
    list_all_dirs = []
    list_all_files = []
    names = ls.listdir(adr)
    for name in names:
        fullname = os.path.join(adr, name) # получаем полное имя
        if os.path.isfile(fullname):
            list_all_files.append(name)
        elif os.path.isdir(fullname):
            list_all_dirs.append(name)
    return list_all_dirs, list_all_files

@bot.message_handler(commands=['start'])
def start(message):
    '''При старте выводим приветствие, и кнопочную панель.'''
    send_mass = str("Привет, " + message.from_user.first_name + "! Ты находишься в файловом менеджере. Выбери действие: ")
    sti = open("system_folder/welcome.webp", 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Создать папку')
    btn2 = types.KeyboardButton('Удалить папку')
    btn3 = types.KeyboardButton('Создать или Изменить файл')
    btn4 = types.KeyboardButton('Удалить файл')
    btn5 = types.KeyboardButton('Прочитать файл')
    btn6 = types.KeyboardButton('Информация о файле')
    btn7 = types.KeyboardButton('Список файлов')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, send_mass, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def start(message):
    '''Условия нажатия кнопок на панели'''
    if message.text == 'Создать папку':
        bot.send_message(message.from_user.id, "Введите название папки: ")
        bot.register_next_step_handler(message, mkdir)
    elif message.text == 'Удалить папку':
        bot.send_message(message.from_user.id, "Введите название папки: ")
        bot.register_next_step_handler(message, rmdir)
    elif message.text == 'Список файлов':
        list_all_dirs, list_all_files = list_all()
        ass = str("Папки: " + "\n" + str(list_all_dirs) + "\n" + " " + "\n" +"Файлы: " + "\n" + str(list_all_files))
        bot.send_message(message.from_user.id, ass)
    elif message.text == 'Создать или Изменить файл':
        bot.send_message(message.from_user.id, "Введите название файла: ")
        bot.register_next_step_handler(message, add)
    elif message.text == 'Удалить файл':
        bot.send_message(message.from_user.id, "Введите название файла: ")
        bot.register_next_step_handler(message, rm)
    elif message.text == 'Прочитать файл':
        bot.send_message(message.from_user.id, "Введите название файла: ")
        bot.register_next_step_handler(message, read)
    elif message.text == 'Информация о файле':
        bot.send_message(message.from_user.id, "Введите название файла: ")
        bot.register_next_step_handler(message, info)
    else:
        sti2 = open("system_folder/choose_action.webp", 'rb')
        bot.send_sticker(message.chat.id, sti2)
        bot.send_message(message.chat.id, "Выбери действие: ")

def mkdir(message):
    '''Создание папки'''
    try:
        name = str(dir.mkdir(adr + message.text))
        bot.send_message(message.from_user.id, "Папка создана.");
    except FileExistsError:
        bot.send_message(message.from_user.id, "Файл/папка с таким именем уже существует.")
def rmdir(message):
    '''Удаление папки'''
    try:
        name = str(dir.rmdir(adr + message.text))
        bot.send_message(message.from_user.id, "Папка удалена.");
    except FileNotFoundError:
        bot.send_message(message.from_user.id, "Такая папка не существует.")
    except NotADirectoryError:
        bot.send_message(message.from_user.id, "Такая папка не существует.")
    except OSError:
        shutil.rmtree(adr + message.text)
        bot.send_message(message.from_user.id, "Папка удалена.")

def add(message):
    '''Создание и/или изменение файла'''
    global name
    name = adr + str(message.text)
    if str(message.text) in ls.listdir(adr):
        if os.path.getsize(name) != 0:
            msg = bot.send_message(message.chat.id, "Файл содержит данные. Чтобы перезаписать нажмите '1'")
            bot.register_next_step_handler(msg, askNum)
        else:
            msg = bot.send_message(message.chat.id, 'Введите текст: ')
            bot.register_next_step_handler(msg, askText)
    else:
        msg = bot.send_message(message.chat.id, 'Введите текст: ')
        bot.register_next_step_handler(msg, askText)
def askNum(message):
    '''Функция обработки запроса на изменение файла'''
    if message.text == '1':
        msg = bot.send_message(message.chat.id, 'Введите текст: ')
        bot.register_next_step_handler(msg, askText)
    else:
        sti2 = open("system_folder/choose_action.webp", 'rb')
        bot.send_sticker(message.chat.id, sti2)
        bot.send_message(message.chat.id, "Выбери действие: ")
def askText(message):
    '''Функция принимающая текст пользователя и записывающая его в файл'''
    try:
        with open(name, 'w',  encoding="utf-8") as f:
            f.write(message.text)
        bot.send_message(message.chat.id, "Текст сохранен.")
    except PermissionError:
        bot.send_message(message.chat.id, "Ошибка доступа.")
    except TypeError:
        msg = bot.send_message(message.chat.id, 'Введите текст: ')
        bot.register_next_step_handler(msg, askText)
def rm(message):
    '''Удаление файла'''
    try:
        name = str(file.rm(adr + message.text))
        bot.send_message(message.from_user.id, "Файл удален.")
    except FileNotFoundError:
        bot.send_message(message.from_user.id, "Данного файла не существует.")
    except PermissionError:
        bot.send_message(message.from_user.id, "Выбранный объект не является файлом. Удаление невозможно.")

def read(message):
    '''Чтение файла'''
    try:
        name = str(adr + message.text)
        with open(name, encoding="utf-8") as f:
            bot.send_message(message.from_user.id,  "--> " + f.read())
    except FileNotFoundError:
        bot.send_message(message.from_user.id,  "Такого файла не существует.")
    except PermissionError:
        bot.send_message(message.from_user.id,  "Ошибка доступа.")
def info(message):
    '''Информация о файле/папке'''
    try:
        name = str(adr + message.text)
        file_info = os.stat(name)
        bot.send_message(message.from_user.id, str(file_info.st_mode) + " - бит защиты")
        bot.send_message(message.from_user.id, str(file_info.st_ino) + " - номер inode")
        bot.send_message(message.from_user.id, str(file_info.st_dev) + " - устройство")
        bot.send_message(message.from_user.id, str(file_info.st_nlink) + " - количество жестких ссылок")
        bot.send_message(message.from_user.id, str(file_info.st_uid) + " - идентификатор пользователя")
        bot.send_message(message.from_user.id, str(file_info.st_gid) + " - идентификатор группы пользователя")
        bot.send_message(message.from_user.id, str(file_info.st_size) + " - размер файла, в байтах")
        bot.send_message(message.from_user.id, str(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_atime))) + " - время последнего доступа")
        bot.send_message(message.from_user.id, str(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_mtime))) + " - время последнего изменения файла")
        bot.send_message(message.from_user.id, str(time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(file_info.st_ctime))) + " - время создания файла")
    except FileNotFoundError:
        bot.send_message(message.from_user.id,  "Такого файла не существует.")

#RunBot
bot.polling(none_stop=True, interval=0)
