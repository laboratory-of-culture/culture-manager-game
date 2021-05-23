#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging


from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
                          
from config import quiz, evaluation

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

INTRO, Q1, A1, Q2, A2, Q3, A3, Q4, A4, Q5, A5, Q6, A6, Q7, A7, Q8, A8, Q9, A9, Q10, A10, Q11,  OUTRO = range(23)

sketch1 = "https://www.dropbox.com/s/l7j8t7ft7l5gnje/1.jpg?dl=0"
sketch2 = "https://www.dropbox.com/s/7o18m3brmhw0fot/2.jpg?dl=0"
sketch3 = "https://www.dropbox.com/s/7ntadxl0sc6fkgy/3.jpg?dl=0"
sketch4 = "https://www.dropbox.com/s/m1ek1tyyzfdykmd/4.jpg?dl=0"
sketch5 = "https://www.dropbox.com/s/kh2zbonxgn58h1c/5.jpg?dl=0"
sketch6 = "https://www.dropbox.com/s/81upimdygc805cx/6.jpg?dl=0"
sketch7 = "https://www.dropbox.com/s/w1y9bx8ojfa28ab/7.jpg?dl=0"
sketch8 = "https://www.dropbox.com/s/f93di2ek7cb84he/8.jpg?dl=0"
sketch9 = "https://www.dropbox.com/s/diavrkf7uahul0y/9.jpg?dl=0"
sketch10 = "https://www.dropbox.com/s/5wf5duyg74grd4q/10.jpg?dl=0"
sketch11 = "https://www.dropbox.com/s/6nu2sum6djgjzk9/11.jpg?dl=0"
label = "https://www.dropbox.com/s/tysxdenphzrdcmk/%D0%BE%D0%B1%D0%BA%D0%BB%D0%B0%D0%B4%D0%B8%D0%BD%D0%BA%D0%B0.jpg?dl=0"
logos = "https://www.dropbox.com/s/2y75to925huzlzg/logos.png?dl=0"





keyboard = ReplyKeyboardMarkup([["1"],["2"],["3"]], one_time_keyboard=True, resize_keyboard=True)

def evaluate(context):
    res = context.user_data['impact-points'] + context.user_data['pleasure-points'] + context.user_data['reputation-points'] 
    print(res)
    if res < -6:
        return "bad"
    
    if res >= -6 and res <= 1:
        return "middle"
    
    if res > 1:
        return "good"

def echo(update, context):
    if update.message.text=="Про гру":
        update.message.reply_text(
        """✋ Авторка: <i>Оксана Чміль</i>\nСкетчі: <i>Наталка Темех</i> \nКод: <i>Андрій Тужиков</i>\n\n Цю симуляційну гру розроблено в рамках проєкту «Культура законності» реалізується за кошти гранту від Посольства Королівства Нідерландів. """, parse_mode=ParseMode.HTML)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=logos)



def print_points(update, context):
        update.message.reply_text(
        """🍀 Користь для громади: <b>{}</b>\n🍦 Власне задоволення: <b>{}</b>\n👏 Репутація: <b>{}</b>""".format(context.user_data['impact-points'], context.user_data['pleasure-points'], context.user_data['reputation-points']), parse_mode=ParseMode.HTML)
    
def results_handler(update, context, Q):
    if update.message.text=="1":
        context.user_data['impact-points'] += quiz[Q]["exp1-impact-points"]
        context.user_data['pleasure-points'] += quiz[Q]["exp1-pleasure-points"]
        context.user_data['reputation-points'] = quiz[Q]["exp1-reputation-points"]
        update.message.reply_text("☝"+quiz[Q]["exp1"])
    
    if update.message.text=="2":
        context.user_data['impact-points'] += quiz[Q]["exp2-impact-points"]
        context.user_data['pleasure-points'] += quiz[Q]["exp2-pleasure-points"]
        context.user_data['reputation-points'] += quiz[Q]["exp2-reputation-points"]
        update.message.reply_text("☝"+quiz[Q]["exp2"])
    
    if update.message.text=="3":
        context.user_data['impact-points'] += quiz[Q]["exp3-impact-points"]
        context.user_data['pleasure-points'] += quiz[Q]["exp3-pleasure-points"]
        context.user_data['reputation-points'] += quiz[Q]["exp3-reputation-points"]
        update.message.reply_text("☝"+quiz[Q]["exp3"])



    

def asker(update, Q):
    update.message.reply_text("❓" + quiz[Q]["question"] + "\n\n" + "1⃣" + quiz[Q]["a1"] + "\n\n" + "2⃣" + quiz[Q]["a2"] + "\n\n" + "3⃣" + quiz[Q]["a3"],
                              reply_markup=keyboard, one_time_keyboard=True)




def start(update, context):
    reply_keyboard = [['Почати', 'Про гру']]
    user = update.message.from_user
    context.bot.send_photo(chat_id=update.message.chat_id, photo=label)

   




    update.message.reply_text(
        """✋ Привіт, <b>{}</b>!\nУявіть, що ви культурний менеджер і у вас є можливість повпливати на громаду своєю діяльністю. Але не забувайте і про власні репуацію та задоволення від процесу, адже без цього вас чекає професійне вигорання.\n\t\t🙏 Отже відповідайте на запитання за покликом серця, але зважайте на параметри “користь для громади”, “власне задоволення” та “репутація”, не дозволяйте цим показникам впасти до критичної цифри. Будьте уважні, адже як би все добре не виходило, результат може бути непередбачуваним.""".format(user.first_name),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True), parse_mode=ParseMode.HTML,)

    return INTRO


def intro(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch1)
    asker(update, "Q1")
    return Q1




def q1(update, context):
    if update.message.text=="1":
        context.user_data['impact-points'] = quiz["Q1"]["exp1-impact-points"]
        context.user_data['pleasure-points'] = quiz["Q1"]["exp1-pleasure-points"]
        context.user_data['reputation-points'] = quiz["Q1"]["exp1-reputation-points"]
        update.message.reply_text(quiz["Q1"]["exp1"])
    
    if update.message.text=="2":
        context.user_data['impact-points'] = quiz["Q1"]["exp2-impact-points"]
        context.user_data['pleasure-points'] = quiz["Q1"]["exp2-pleasure-points"]
        context.user_data['reputation-points'] = quiz["Q1"]["exp2-reputation-points"]
        update.message.reply_text(quiz["Q1"]["exp2"])
    
    if update.message.text=="3":
        context.user_data['impact-points'] = quiz["Q1"]["exp3-impact-points"]
        context.user_data['pleasure-points'] = quiz["Q1"]["exp3-pleasure-points"]
        context.user_data['reputation-points'] = quiz["Q1"]["exp3-reputation-points"]
        update.message.reply_text(quiz["Q1"]["exp3"])

    print_points(update,context)

    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))

    return A1

def a1(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch2)
    asker(update,"Q2")
    

    return Q2



def q2(update, context):
    results_handler(update,context,"Q2") 
    print_points(update,context)

    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))           
    return A2

def a2(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch3)
    asker(update,"Q3")

    return Q3

def q3(update, context):
    results_handler(update,context,"Q3") 
    print_points(update,context)

    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))       
    return A4

def a3(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch4)
    asker(update,"Q4")

    return Q4


def q4(update, context):
    results_handler(update,context,"Q4") 
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))      
    return A4

def a4(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch5)
    asker(update,"Q5")

    return Q5

def q5(update, context):
    results_handler(update,context,"Q5")
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))   

    return A5

def a5(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch6)
    asker(update,"Q6")

    return Q6


def q6(update, context):
    results_handler(update,context,"Q6")
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))   
    return A6

def a6(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch7)
    asker(update,"Q7")

    return Q7



def q7(update, context):
    results_handler(update,context,"Q7")
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))   


    return A7

def a7(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch8)
    asker(update,"Q8")

    return Q8


def q8(update, context):
    results_handler(update,context,"Q8")
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))   
    return A8

def a8(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch9)
    asker(update,"Q9")

    return Q9

def q9(update, context):
    results_handler(update,context,"Q9")
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))   
    return A9


def a9(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch10)
    asker(update,"Q10")

    return Q10

def q10(update, context):
    results_handler(update,context,"Q10")
    print_points(update,context)
    update.message.reply_text(
        "Граємо далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))   

    return A10

def a10(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch11)
    asker(update,"Q11")

    return Q11


def q11(update, context):
    results_handler(update,context,"Q11")
    update.message.reply_text(evaluation[evaluate(context)], parse_mode=ParseMode.HTML )
    print_points(update,context)
    update.message.reply_text("Грати знову - /start")

    return ConversationHandler.END



def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1347548081:AAGM95zgf5A4ZJqhed66OMHyxK91Tdch6Ec", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INTRO: [MessageHandler(Filters.regex('^(Почати)$'), intro)],

            Q1: [MessageHandler(Filters.text, q1)],
            Q2: [MessageHandler(Filters.text, q2)],
            Q3: [MessageHandler(Filters.text, q3)],
            Q4: [MessageHandler(Filters.text, q4)],
            Q5: [MessageHandler(Filters.text, q5)],
            Q6: [MessageHandler(Filters.text, q6)],
            Q7: [MessageHandler(Filters.text, q7)],
            Q8: [MessageHandler(Filters.text, q8)],
            Q9: [MessageHandler(Filters.text, q9)],
            Q10: [MessageHandler(Filters.text, q10)],
            Q11: [MessageHandler(Filters.text, q11)],

            A1: [MessageHandler(Filters.text, a1)],
            A2: [MessageHandler(Filters.text, a2)],
            A3: [MessageHandler(Filters.text, a3)],
            A4: [MessageHandler(Filters.text, a4)],
            A5: [MessageHandler(Filters.text, a5)],
            A6: [MessageHandler(Filters.text, a6)],
            A7: [MessageHandler(Filters.text, a7)],
            A8: [MessageHandler(Filters.text, a9)],
            A9: [MessageHandler(Filters.text, a9)],
            A10: [MessageHandler(Filters.text, a10)],
            

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    echo_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(echo_handler)
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()