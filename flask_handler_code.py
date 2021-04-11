import telebot
from flask import Flask, request
import setup
import bot_code

secret = setup.bot_secret()
url = 'https://matanovezno.pythonanywhere.com/' + secret
bot = telebot.TeleBot(setup.bot_token(), threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url)

app = Flask(__name__)

@app.route('/')
def site():
    return 'Welcome!'


@app.route('/'+secret, methods=['POST'])
def webhook():
    update=telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=[""'start', 'help', 'report', 'question', 'parameters',
                              'task', 'add', 'stat', 'top', 'paradd', 'ban'""])
def command_sorting(message):
    print(message)
    if message.chat.id != -1001382702607 and message.chat.id != -1001415917929 and message.chat.id != -1001418192939:
        # -1001288947031 test group
        if message.chat.type == 'private':
            bot.reply_to(message, 'Бот можна використовувати лише у группі @matan_help')
        else:
            try:
                bot.leave_chat(message.chat.id)
            except:
                pass
    else:
        if str(message.text) == '/start':
            bot_code.start_message(bot, message)
        elif str(message.text)[:5] == '/help':
            bot_code.help_message(bot, message)
        elif str(message.text) == '/report':
            bot_code.report_message(bot, message)
        elif str(message.text) == '/question':
            bot_code.question_message(bot, message)
        elif str(message.text) == '/parameters':
            bot_code.parameters_text(bot, message)
        elif str(message.text)[:5] == '/task':
            bot_code.task_text(bot, message)
        elif str(message.text)[:4] == '/add':
            bot_code.add_task(bot, message)
        # elif str(message.text) == '/stat':
        #     bot_code.url_send(bot, message)
        elif str(message.text)[:4] == '/top':
            bot_code.top_10(bot, message)
        elif str(message.text)[:7] == '/paradd':
            bot_code.add_param(bot, message)
        elif str(message.text)[:4] == '/ban':
            msg = message.from_user.id
            if msg == 416859943 or msg == 560939857 or msg == 515912635 or msg == 618831393 or msg == 406855987:
                bot_code.ban_command(bot, message)
            else:
                bot_code.ban_list(bot, message)
        else:
            pass


@bot.message_handler(content_types=[""'video_note', 'voice', 'sticker', 'audio', 'document', 'photo', 'text',
                                    'video', 'location', 'contact', 'new_chat_members', 'left_chat_member'""])
def message_sorting(message):
    print(message)
    if message.chat.id != -1001382702607 and message.chat.id != -1001415917929 and message.chat.id != -1001418192939:
        # -1001288947031 test group
        if message.chat.type == 'private':
            bot.reply_to(message, 'Бот можна використовувати лише у группі @matan_help')
        else:
            try:
                bot.leave_chat(message.chat.id)
            except:
                pass
    else:
        bot_code.queue(bot, message)
        if message.content_type == 'new_chat_members':
            bot_code.hello_message(bot, message)
        elif message.content_type == 'text':
            bot_code.send_text(bot, message)
        elif message.content_type == 'photo':
            bot_code.handle_docs_photo(bot, message)
        else:
            pass
