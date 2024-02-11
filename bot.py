import telebot
import proc
import config


# telegram bot API
bot = telebot.TeleBot(config.TOKEN)


# says hello to user isung their name and last name if exists
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.last_name == None:
        mess = f'Hello, <b>{message.from_user.first_name}</b>. '
    else:
        mess = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>. '
    caller_info = [message.from_user.id, message.from_user.first_name, message.from_user.last_name]
    mess = mess + proc.add_caller(caller_info) # adds caller info as a row to the google spreadsheet, if the user doesn't exist
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['give_5_contacts'])
def give_5_contacts(message):
    free_contacts = proc.empty_contacts() #list of contacts, that don't have field 'Caller'

    if len(free_contacts) < 1:
        bot.send_message(message.chat.id, 'There are no free contacts to call')
    else:
        if len(free_contacts) < 5:
            N = len(free_contacts)
        else:
            N = 5
    for i in range(N):
        mess =', '.join(free_contacts[i][:6]) 
        print(mess)
        proc.add_caller_to_contact(free_contacts[i], message.from_user.first_name)
        bot.send_message(message.chat.id, mess)

'''
@bot.message_handler(commands=['start'])
def good_night(message):
    mess = 'Message'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    mess = 'Message'
    bot.send_message(message.chat.id, message.text + mess)
'''

bot.infinity_polling()
