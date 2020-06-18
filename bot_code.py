# _*_ coding: UTF-8 _*_

import random
import time
import pymysql
from collections import deque
import math


q = deque()
path = ""
isSolving = False
rightAnswer = 0
level = 0
tm = 0
tmpar = 0
isPAdd = False
isAdd = False
add_level = 0
add_ans = 0
add_lvls_list = [0, 0, 0, 0, 0]
antirepeat = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
PrevHelloMessageId = 101437
NewHelloMessageId = 101438  # message_id
helloText = """Вітаю в @matan_help ✋
Головні правила чату:
➡️Не ображати інших учасників
➡️Допомагати іншим учасникам, якщо маєте змогу
➡️Якщо вам потрібна допомога, то просто попросіть
➡️За рекламу інших сторінок - бан🚫
/help - доступні команди
Бажаємо вам 200 балів на ЗНО!"""
helpText = """ /report - повідомити про порушення
/question - якщо виникло питання
/task [складність]- розв'язуй задачі, стань першим в рейтингу(складність варіюється від 1 до 4, де 1-найлегший рівень)
/top [msg або intel]- топ 10 учасників чату(msg-сортування за кілкістю повідомлень, intel-за інтелектуальним рейтингом)
/ban- перевір, чи можеш ти вирішувати наші завдання."""


def rnd(x):
    if x == 0:
        return 0
    y = abs(x) * 10000.0
    if math.floor(y) % 10 >= 5:
        y += 10.0
    y /= 10.0
    y = math.floor(y)
    y = (x / abs(x)) * y / 1000.0
    return y


def trueRandom(a, lvl):
    rndval = random.randint(1, a)
    for i in antirepeat[lvl - 1]:
        if i == rndval:
            return trueRandom(a, lvl)
    for i in range(1, 20):
        antirepeat[lvl - 1][i - 1] = antirepeat[lvl - 1][i]
    antirepeat[lvl - 1][i] = rndval
    return rndval


def pts():
    tm1 = int(time.time()) - int(tm)
    return round(
        pow(2, (level - 1) / 2.0) * pow(3, float(level) - float(tm1 / (120.0 * pow(10, float(level + 2) / 3.0)))))


def start_message(bot, message):
    try:
        bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help')
    except:
        pass


def help_message(bot, message):
    try:
        bot.send_message(message.chat.id, helpText)
    except:
        pass


def report_message(bot, message):
    try:
        bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @MatHtaM @melkii_pumba')
        bot.send_message(-1001418192939, 'Розбійник в @matan_help')
    except:
        pass


def question_message(bot, message):
    try:
        bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @MatHtaM @melkii_pumba')
        bot.send_message(-1001418192939, 'Дебіл в @matan_help')
    except:
        pass


# def parameters_text(bot, message):
# 	global tmpar
# 	if time.time()-tmpar>600:
# 		tmpar=time.time()
# 		listQ = open("/home/matanovezno/Data/Tasks/q.txt", 'r')
# 		counter=0
# 		quantity=0
# 		for line in listQ:
# 			counter+=1
# 			if counter==5:
# 				quantity=int(line)
# 		a = random.randint(1, quantity)
# 		pth = r"/home/matanovezno/Data/Tasks/Questions/5/" + str(a) + ".png"
# 		file = open(pth, 'rb')
# 		bot.send_photo(message.chat.id, file, caption="Розв'язання цих задач на параметри не впливає на інтелектуальний рейтинг. Тут ви можете знайти лише вибрані задачі підвищеної складності. Викликати іншу задачу можна лише через 10 хвилин після виклику даної задачі. Відповідь автоматично не перевіряється.")


def task_text(bot, message):
    global isSolving
    global rightAnswer
    global path
    global level
    global tm
    tester = 0
    tm1 = time.time()
    conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                          password="P@ssw0rd", database="matanovezno$Matanove")
    cur = conn.cursor()
    if int(tm1) - int(tm) > 600 * level:
        isSolving = False
    try:
        tester = int(message.text[6:])
    except:
        bot.reply_to(message,
                     'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
        return 0
    cur.execute("SELECT user_id FROM stat WHERE isbanned = 1")
    users_ban_id = cur.fetchall()
    banned = []
    for user_ban_id in users_ban_id:
        banned.append(user_ban_id[0])
    if not isSolving and (tester == 1 or tester == 2 or tester == 3 or tester == 4):
        if message.from_user.id not in banned:
            listQ = open("/home/matanovezno/Data/Tasks/q.txt", 'r')
            quantity = 0
            counter = 0
            for line in listQ:
                counter += 1
                if counter == int(message.text[6]):
                    level = int(message.text[6])
                    quantity = int(line)
            a = trueRandom(quantity, level)
            path = r"/home/matanovezno/Data/Tasks/Questions/" + message.text[6] + "/" + str(a) + ".png"
            file = open(path, 'rb')
            try:
                bot.send_photo(message.chat.id, file,
                              caption='Відповіддю є число в десятковому записі. Відповідь округлюється до трьох знаків після коми за правилами округлення.\nРівень складності: ' + str(
                                  level) + '\nПриклад: 16; -38,8; 0; 44.268. \nТермін виконання - ' + str(
                                  level * 10) + ' хвилин')
            except:
                pass
            isSolving = True
            path2 = "/home/matanovezno/Data/Tasks/Solutions/" + str(level) + "/sol.txt"
            counter = 0
            sol = open(path2, 'r')
            for line in sol:
                counter += 1
                if counter == a:
                    rightAnswer = line
            file.close()
            sol.close()
            listQ.close()
            tm = time.time()
        else:
            bot.reply_to(message, 'Ви не можете вирішувати завдання')
    elif isSolving:
        file = open(path, 'rb')
        try:
            bot.send_photo(message.chat.id, file, caption=r"Спочатку розв'яжіть запропоновану задачу!")
        except:
            pass
    else:
        try:
            bot.reply_to(message,
                         'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
        except:
            pass
        return 0
    conn.commit()
    cur.close()


def add_task(bot, message):
    global add_level
    global add_ans
    global isAdd
    if int(message.chat.id) != -1001382702607:
        try:
            bot.reply_to(message, 'На жаль, Ви не маєте прав додавати завдання до боту')
        except:
            pass
        return 0
    try:
        add_level = int(message.text[5])
        add_ans = message.text[7]
        add_ans = float(message.text[7:].replace(',', '.'))
        isAdd = True
    except:
        bot.reply_to(message, 'Невірні аргументи')
        return 0
    f = open('/home/matanovezno/Data/Tasks/q.txt', 'r')
    counter = 0
    for line in f:
        add_lvls_list[counter] = int(line)
        counter += 1
    add_lvls_list[add_level - 1] += 1
    f.close()
    bot.reply_to(message, 'Ожидаю фото...')


# def url_send(bot, message):
#     url = ''
#     try:
#         bot.reply_to(message, url)
#     except:
#         pass


def top_10(bot, message):
    # print(msg)
    sort = message.text[5:]
    sort = sort.replace(" ", "")
    # print(sort)
    conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                          password="P@ssw0rd", database="matanovezno$Matanove")
    cur = conn.cursor()
    if sort == "msg":
        msg = str('Рейтинг за кілкістю повідомлень\n')
        cur.execute("SELECT t1.name, t1.surname, t2.qty FROM identify=t1, stat=t2 WHERE t1.user_id = t2.user_id ORDER BY t2.qty DESC")
        top_name = cur.fetchmany(size=10)
        # print(top_name)
        counter = 1
        for person in top_name:
            msg += '<b><i>' + str(counter) + '. '
            msg += '</i></b>' + str(person[0]) + ' '
            msg += (str(person[1]) + ' - ', '- ')[person[1] == '']
            msg += '<b>' + str(person[2]) + '</b>\n'
            counter += 1
        # print(msg)
        try:
            bot.reply_to(message, msg, parse_mode="HTML")
        except:
            pass
    elif sort == "intel":
        msg = str('Інтелектуальний рейтинг\n')
        cur.execute("SELECT t1.name, t1.surname, t2.intel FROM identify=t1, stat=t2 WHERE t1.user_id = t2.user_id ORDER BY t2.intel DESC")
        top_name = cur.fetchmany(size=10)
        # print(top_name)
        counter = 1
        for person in top_name:
            msg += '<b><i>' + str(counter) + '. '
            msg += '</i></b>' + str(person[0]) + ' '
            msg += (str(person[1]) + ' - ', '- ')[person[1] == '']
            msg += '<b>' + str(person[2]) + '</b>\n'
            counter += 1
        # print(msg)
        try:
            bot.reply_to(message, msg, parse_mode="HTML")
        except:
            pass
    else:
        try:
            bot.reply_to(message,
                         'Вказані невірні аргументи. Аргументом може слугувати лише msg або intel')
        except:
            pass
    conn.commit()
    cur.close()

def ban_command(bot, message):
    sort = message.text[5:]
    sort = sort.replace(" ", "")
    conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                          password="P@ssw0rd", database="matanovezno$Matanove")
    cur = conn.cursor()
    if sort == 'add' and message.reply_to_message != 'None':
        try:
            user_ban_id = message.reply_to_message.from_user.id
            cur.execute(f"UPDATE stat SET isbanned = 1 WHERE user_id = '{user_ban_id}'")
            msg = ''
            msg += str(message.reply_to_message.from_user.first_name) + ' '
            msg += (str(message.reply_to_message.from_user.last_name) + ' ', '')[str(message.reply_to_message.from_user.last_name) == 'None']
            msg += 'тепер не може вирішувати задачі'
            bot.reply_to(message, msg)
        except:
            pass
    if sort == 'rm' and message.reply_to_message != 'None':
        try:
            user_ban_id = message.reply_to_message.from_user.id
            cur.execute(f"UPDATE stat SET isbanned = 0 WHERE user_id = '{user_ban_id}'")
            msg = ''
            msg += str(message.reply_to_message.from_user.first_name) + ' '
            msg += (str(message.reply_to_message.from_user.last_name) + ' ', '')[str(message.reply_to_message.from_user.last_name) == 'None']
            msg += 'тепер може вирішувати задачі'
            bot.reply_to(message, msg)
        except:
            pass
    else:
        pass
    conn.commit()
    cur.close()


def ban_list(bot, message):
    conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                          password="P@ssw0rd", database="matanovezno$Matanove")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM stat WHERE isbanned = 1")
    users_ban_id = cur.fetchall()
    banned = []
    for user_ban_id in users_ban_id:
        banned.append(user_ban_id[0])
    if message.from_user.id in banned:
        bot.reply_to(message, 'Ви не можете вирішувати задачі')
    else:
        bot.reply_to(message, 'Ви можете вирішувати задачі')

def add_param(bot, message):
    global isPAdd
    if int(message.chat.id) != -1001382702607:
        try:
            bot.reply_to(message, 'На жаль, Ви не маєте прав додавати завдання до боту')
        except:
            pass
        return 0
    f = open('/home/matanovezno/Data/Tasks/q.txt', 'r')
    counter = 0
    for line in f:
        add_lvls_list[counter] = int(line)
        counter += 1
    add_lvls_list[4] += 1
    isPAdd = True
    bot.reply_to(message, 'Приму параметры только если Илона отсосёт...')


# Новий учасник групи зайшов в чат
def hello_message(bot, message):
    try:
        bot.reply_to(message, helloText)
    except:
        pass
    global PrevHelloMessageId
    global NewHelloMessageId
    PrevHelloMessageId = int(NewHelloMessageId)
    NewHelloMessageId = int(message.message_id) + 1
    try:
        bot.delete_message(message.chat.id, PrevHelloMessageId)
    except:
        pass


def send_text(bot, message):
    global isSolving
    tm1 = time.time()
    txt = message.text
    conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                          password="P@ssw0rd", database="matanovezno$Matanove")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM stat WHERE isbanned = 1")
    users_ban_id = cur.fetchall()
    banned = []
    for user_ban_id in users_ban_id:
        banned.append(user_ban_id[0])
    txt = txt.replace(',', '.')
    if int(tm1) - int(tm) > 600 * level:
        isSolving = False
    try:
        float(txt)
        isVal = True
    except ValueError:
        isVal = False
    if isVal:
        if isSolving and float(rnd(float(txt))) == float(rnd(float(rightAnswer))) and message.from_user.id not in banned:
            try:
                bot.reply_to(message,
                             '<b>Вітаємо!</b> <i>Ви першим розв\'язали задачу рівня ' + str(level) + ' за <b>' + str(
                                 int(tm1) - int(tm)) + ' с</b>, і отримуєте</i> <b>+' + str(
                                 pts()) + '</b> <i>до Вашого інтелектуального рейтингу</i>', parse_mode="HTML")
            except:
                pass
            isSolving = False
            intelligence(bot, message, pts())
    conn.commit()
    cur.close()


def handle_docs_photo(bot, message):
    global isAdd
    global isPAdd
    if isAdd and message.chat.id == -1001382702607:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = "/home/matanovezno/Data/Tasks/Questions/" + str(add_level) + "/" + str(
                add_lvls_list[add_level - 1]) + ".png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                bot.reply_to(message, "Ok!")
            f = open("/home/matanovezno/Data/Tasks/q.txt", 'w')
            for i in add_lvls_list:
                f.write(str(i) + '\n')
            f.close()
            f = open("/home/matanovezno/Data/Tasks/Solutions/" + str(add_level) + "/sol.txt", 'a')
            f.write('\n' + str(add_ans))
            isAdd = False
        except Exception as e:
            bot.reply_to(message, e)
    if isPAdd and message.chat.id == -1001382702607:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = "/home/matanovezno/Data/Tasks/Questions/5/" + str(add_lvls_list[add_level - 1]) + ".png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                bot.reply_to(message, "Илона отлично сосёт!")
            f = open("/home/matanovezno/Data/Tasks/q.txt", 'w')
            for i in add_lvls_list:
                f.write(str(i) + '\n')
            f.close()
            isPAdd = False
        except Exception as e:
            bot.reply_to(message, e)


def queue(bot, message):
    if message.chat.id == -1001415917929 and message.from_user.id != 777000:  # Matanove
    # if message.chat.id == -458266883 and message.from_user.id != 777000:    #testgroup
    # if message.chat.id == -1001418192939 and message.from_user.id != 777000:    #troll
        q.append(message)
        while len(q) > 0:
            mssg = q.popleft()
            conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                                  password="P@ssw0rd", database="matanovezno$Matanove")
            cur = conn.cursor()
            name = (str(mssg.from_user.first_name), "")[str(mssg.from_user.first_name) == "None"]
            name_in_sql = conn.escape_string(name)
            print(name_in_sql)
            surname = (str(mssg.from_user.last_name), "")[str(mssg.from_user.last_name) == "None"]
            surname_in_sql = conn.escape_string(surname)
            print(surname_in_sql)
            user_id = mssg.from_user.id
            cur.execute(f"SELECT user_id FROM identify WHERE user_id = '{user_id}'")
            user_id_list = cur.fetchall()
            if len(user_id_list) == 1:
                # print(name + "1")
                cur.execute(f"UPDATE stat SET qty = qty + 1 WHERE user_id = '{user_id}'")
            elif len(user_id_list) == 0:
                # print(name + "2")
                cur.execute(f"INSERT INTO identify VALUES ('{name_in_sql}', '{surname_in_sql}', '{user_id}')")
                cur.execute(f"INSERT INTO stat (qty, user_id) VALUES (1, '{user_id}')")
            else:
                # print(name + "3")
                cur.execute(f"SELECT * FROM stat WHERE user_id = '{user_id}'")
                user_false_list = cur.fetchone()
                cur.execute(f"DELETE FROM stat WHERE user_id = '{user_id}'")
                cur.execute(
                    f"INSERT INTO stat VALUES ('{user_false_list[0]}', '{user_false_list[1]}', '{user_false_list[2]}')")
                cur.execute(f"UPDATE stat SET qty = qty + 1 WHERE user_id = '{user_id}'")
                cur.execute(f"SELECT * FROM identify WHERE user_id = '{user_id}'")
                user_false_list1 = cur.fetchone()
                cur.execute(f"DELETE FROM identify WHERE user_id = '{user_id}'")
                cur.execute(
                    f"INSERT INTO identify VALUES ('{user_false_list1[0]}', '{user_false_list1[1]}', '{user_false_list1[2]}')")
            conn.commit()
            cur.close()
    else:
        pass


def intelligence(bot, message, intel):
    if message.chat.id == -1001415917929 and message.from_user.id != 777000:  # Matanove
    # if message.chat.id == -458266883 and message.from_user.id != 777000:    #testgroup
    # if message.chat.id == -1001418192939 and message.from_user.id != 777000:    #troll
        try:
            # print(intel)
            conn = pymysql.connect(host="matanovezno.mysql.pythonanywhere-services.com", user="matanovezno",
                                  password="P@ssw0rd", database="matanovezno$Matanove")
            cur = conn.cursor()
            user_id = message.from_user.id
            cur.execute(f"UPDATE `stat` SET `intel` = `intel` + {intel} WHERE `user_id` = '{user_id}'")
            conn.commit()
            cur.close()
        except:
            pass
    else:
        pass

