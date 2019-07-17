from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from game import WordGenerator
import os
wg = WordGenerator()

word = wg.generate_word()
guess_word = "-" * len(word)
uniq_letters = set(word)
chance = len(uniq_letters)
used_letters = set()


def get_help(bot, update):
    global guess_word, chance
    chat_id = update.effective_user.id
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
    message = "You gave your life for one letter:\n {}\n{}".format(guess_word.upper(), ("❤️" * chance))
    bot.send_message(chat_id, message)


def get_info(bot, update):
    user = update.effective_user.name
    message = "Hi, {}!\nPress /help to get hint \nYou will lose one life for one hint.".format(user)
    bot.send_message(update.effective_user.id, message)


def start(bot, update):
    message = "*Press any letter to start our game...*\n*To get more information press - /info*"
    bot.send_message(update.effective_user.id, message, parse_mode='Markdown')
    check_the_letter(bot, update)


def restart_game():
    global word, guess_word, chance, uniq_letters, used_letters
    word = wg.generate_word()
    guess_word = "-" * len(word)
    uniq_letters = set(word)
    chance = len(uniq_letters)
    used_letters = set()


def check_the_letter(bot, update):

    global word, guess_word, chance, used_letters
    chat_id = update.effective_user.id
    user_input = update.message.text.lower()
    if len(user_input) > 1 and user_input != "/start":
        if user_input.lower() == word:
            bot.send_message(chat_id, "🎉🎊You nailed!!!🎉🎊")
        else:
            bot.send_message(chat_id, "❗️❗️❗You lose❗️❗️❗️\n{}".format(word))
        restart_game()
    elif len(user_input) == 1:
        if user_input in word:
            index = -1
            for letter in word:
                if user_input == letter:
                    index = word.index(user_input, index + 1)
                    guess_word = guess_word[:index] + user_input + guess_word[index + 1:]
            used = ', '.join(used_letters)
            text = "✅\n" + "Wrong letters: " + used + "\n*" + guess_word.upper() + "*\n\n" + ("❤️" * chance)
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
                text = "❌\n" + "Wrong letters: " + used + "\n*" + guess_word.upper() + "*\n\n" + ("❤️" * chance)
                bot.send_message(chat_id, text, reply_to_message_id=update.message.message_id, parse_mode='Markdown')


token = os.environ['guess_word']

updater = Updater(token)

help_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(CommandHandler('help', get_help))
updater.dispatcher.add_handler(CommandHandler('info', get_info))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=check_the_letter))

updater.start_polling()
updater.idle()
