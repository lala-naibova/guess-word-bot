from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from game import WordGenerator
from message_utils import b, i, hearts
from oxford_dict import DefinitionProvider
import os
wg = WordGenerator()

word = wg.generate_word().upper()
guess_word = "-" * len(word)
chance = len(set(word))
used_letters = set()
can_help = False
dp = DefinitionProvider(api_key='25eb93d4f4a50827a04294a5967c7c03', app_id='544b9168')

information = dp.get_definition(word)


def ask_letter(bot, update):
    global guess_word, chance
    chat_id = update.effective_user.id
    if chance == 1:
        bot.send_message(chat_id, "Dear, {}, u have only 1 life ☹️".format(update.effective_user.name))
        return
    chance -= 1
    for i in range(len(word)):
        if guess_word[i] == '-':
            lett = word[i]
            index = i
            for letter in word:
                if lett == letter:
                    guess_word = guess_word[:index] + word[index] + guess_word[index + 1:]
                    index = word.find(lett, index + 1)
                    if index == -1:
                        break
            break
    message = "You gave your life for one letter:\n {}\n{}".format(guess_word, hearts(chance))
    bot.send_message(chat_id, message)


def get_info(bot, update):
    user = update.effective_user.name
    message = "**Press /letter to get letter \nYou will lose one life." \
              "\n**Press /help to get meaning of the word (You can use it only ones)\nYou will lose one life.".format(user)
    bot.send_message(update.effective_user.id, message)


def start(bot, update):
    name = update.effective_user.name
    message = "Dear, _{}_,\n What am I ? - {}\nTo get more information press - _/info_".format(name, information['definition'])
    bot.send_message(update.effective_user.id, message, parse_mode='Markdown')
    check_the_letter(bot, update)


def restart_game():
    global word, guess_word, chance, used_letters, can_help, information
    word = wg.generate_word().upper()
    guess_word = "-" * len(word)
    chance = len(set(word))
    used_letters = set()
    information = dp.get_definition(word)
    can_help = False


def get_help(bot, update):
    global chance, guess_word, can_help
    chat_id = update.effective_user.id
    name = update.effective_user.name
    if can_help:
        message = 'You have used this action.'
        bot.send_message(chat_id, message)
        return
    if chance < 2:
        message = '{}, you cannt use this help, case of ur life'.format(name)
        bot.send_message(chat_id, message)
    else:
        chance -= 1
        message = '2nd description : {}\nYou gave your life\n {}\n{}'.format(information['hint'], guess_word, hearts(chance))
        bot.send_message(chat_id, message)
    can_help = True


def check_the_letter(bot, update):

    global word, guess_word, chance, used_letters
    chat_id = update.effective_user.id
    user_input = update.message.text.upper()
    if len(user_input) > 1 and user_input != "/START":
        if user_input.upper() == word:
            bot.send_message(chat_id, "🎉🎊You nailed!!!🎉🎊")
        else:
            bot.send_message(chat_id, "❗️❗️❗You lose❗️❗️❗️\nThe word was '{}'".format(b(word)))
        restart_game()
    elif len(user_input) == 1:
        if user_input in word:
            index = -1
            for letter in word:
                if user_input == letter:
                    index = word.index(user_input, index + 1)
                    guess_word = guess_word[:index] + user_input + guess_word[index + 1:]
            used = ', '.join(used_letters)
            text = "✅\n" + "Wrong letters: " + used + "\n" + b(guess_word) + "\n\n" + hearts(chance)
            if guess_word == word:
                text = "🎉🎊Yeah, {} , u did it - {}🎉🎊".format(update.effective_user.name, guess_word)
                restart_game()
            bot.send_message(chat_id, text, reply_to_message_id=update.message.message_id, parse_mode='Markdown')
        else:
            chance -= 1
            if not chance:
                bot.send_message(chat_id, "❗️❗️❗You lose❗️❗️❗️\n{}".format(word))
                restart_game()
            else:
                used_letters.add(user_input)
                used = ', '.join(used_letters)
                text = "❌\n" + "Wrong letters: " + used + "\n" + b(guess_word) + "\n\n" + hearts(chance)
                bot.send_message(chat_id, text, reply_to_message_id=update.message.message_id, parse_mode='Markdown')


token = os.environ['guess_word']

updater = Updater(token)

help_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(CommandHandler('letter', ask_letter))
updater.dispatcher.add_handler(CommandHandler('help', get_help))
updater.dispatcher.add_handler(CommandHandler('info', get_info))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=check_the_letter))

updater.start_polling()
updater.idle()
