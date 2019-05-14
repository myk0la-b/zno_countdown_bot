# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import Updater
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import InlineQueryResultCachedSticker
from telegram import Bot
from datetime import datetime
from random import randint
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import os


load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID_ME = int(os.getenv('CHAT_ID_ME'))
ZNO_DATE_MATH = datetime.strptime(os.getenv('ZNO_DATE_MATH_ISO_STR'), '%Y-%m-%d')
ZNO_DATE_UKR = datetime.strptime(os.getenv('ZNO_DATE_UKR_ISO_STR'), '%Y-%m-%d')
ZNO_DATE_ENG = datetime.strptime(os.getenv('ZNO_DATE_ENG_ISO_STR'), '%Y-%m-%d')
ZNO_DATE_PHYSICS = datetime.strptime(os.getenv('ZNO_DATE_PHYSICS_ISO_STR'), '%Y-%m-%d')

try:
    f = open('ids.cnf', 'r')
    line = f.readline()
    print(line)
    resId = int(line)
    f.close()
except FileNotFoundError:
    f = open('ids.cnf', 'w')
    resId = 0
    f.write(str(resId))


def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
    update.message.reply_text('chat id: {}\nuid: {}'.format(update.message.chat.id, update.message.from_user.id))


def get_sticker_id_with_text(bot, text: str,):
    try:
        img = Image.open('bear.webp')
    except IOError:
        print('IOError')

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('MPLUSRounded1c-Medium.ttf', size=100)

    line_max_length = 21
    res_text = ''
    wrap_num_a = 0
    wrap_num_b = 0
    while wrap_num_a + line_max_length < text.__len__():
        for i in range(wrap_num_a, min(wrap_num_a + line_max_length, text.__len__())):
            if text[i] == ' ':
                wrap_num_a = i + 1
            elif text[i] == '.':
                wrap_num_a = i
            # print(wrap_num_a)

        res_text += text[wrap_num_b:wrap_num_a] + '\n'
        wrap_num_b = wrap_num_a
    res_text += text[wrap_num_b:]

    draw.text((50, 20), font=font, text=res_text, fill=(0 + randint(0, 255), 0 + randint(0, 128),
                                                        0 + randint(0, 255), 200))
    img.save('bb.webp')
    doc = open('bb.webp', 'rb')
    message = bot.send_document(chat_id=CHAT_ID_ME, document=doc)
    return message.sticker.file_id


def inline(bot, update):
    global resId
    delta_ukr = ZNO_DATE_UKR - datetime.today()
    delta_math = ZNO_DATE_MATH - datetime.today()
    delta_eng = ZNO_DATE_ENG - datetime.today()
    delta_physics = ZNO_DATE_PHYSICS - datetime.today()
    days_ukr = delta_ukr.days
    days_math = delta_math.days
    days_eng = delta_eng.days
    days_physics = delta_physics.days

    day_rus = list(['дней', 'день', 'дня', 'дня', 'дня', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней'])
    # soon
    # day_eng = list()
    day_ukr = list(['днів', 'день', 'дні', 'дні', 'дні', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів', 'днів'])

    warn_rus = list(['Берегись', 'Осторожнее', 'Спасайся', 'Беги', 'Учись', 'Пора', 'А мама говорила'])
    warn_ukr = list(['Тікай у село', 'Обережніше', 'Рятуйся', 'Ну ЗНУ це теж ЗВО', 'Починай готуватися', 'Готуй бабки',
                     'Солдат. Звучить не так і погано', 'Батько тебе породив, він тебе і вб\'є'])

    text = update.inline_query.query

    result = 'До ЗНО осталось {} {}, а ты {}.'.format(days_ukr, day_rus[days_ukr % 20], text)

    if text == '':
        warn_num = randint(0, warn_rus.__len__())
        result = 'До ЗНО осталось {} {}. {}.'.format(days_ukr, day_rus[days_ukr % 20], warn_rus[warn_num])

    query_result_rus = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Countdown Russian',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    result = 'До ЗНО з математики залишилось {} {}, а ти {}.'.format(days_math, day_ukr[days_math % 20], text)
    if text == '':
        warn_num = randint(0, warn_ukr.__len__())
        result = 'До ЗНО з математики залишилось {} {}. {}.'.format(days_math, day_ukr[days_math % 20], warn_ukr[warn_num])

    query_result_ukr_math = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Зворотній відлік математика',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    id_math = get_sticker_id_with_text(bot, result)
    query_result_sticker_math = InlineQueryResultCachedSticker(type='sticker', id=resId, sticker_file_id=id_math)
    resId += 1

    result = 'До ЗНО з української залишилось {} {}, а ти {}.'.format(days_ukr, day_ukr[days_ukr % 20], text)
    if text == '':
        warn_num = randint(0, warn_ukr.__len__())
        result = 'До ЗНО з української залишилось {} {}. {}.'.format(days_ukr, day_ukr[days_ukr % 20],
                                                                     warn_ukr[warn_num])
    query_result_ukr_ukr = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Зворотній відлік українська',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    id_ukr = get_sticker_id_with_text(bot, result)
    query_result_sticker_ukr = InlineQueryResultCachedSticker(type='sticker', id=resId, sticker_file_id=id_ukr)
    resId += 1

    #
    # English
    #
    result = 'До ЗНО з англійської залишилось {} {}, а ти {}.'.format(days_eng, day_ukr[days_eng % 20], text)
    if text == '':
        warn_num = randint(0, warn_ukr.__len__())
        result = 'До ЗНО з англійської залишилось {} {}. {}.'.format(days_eng, day_ukr[days_eng % 20],
                                                                     warn_ukr[warn_num])
    query_result_ukr_eng = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Зворотній відлік англійська',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    id_ukr = get_sticker_id_with_text(bot, result)
    query_result_sticker_eng = InlineQueryResultCachedSticker(type='sticker', id=resId, sticker_file_id=id_ukr)
    resId += 1

    #
    # Physics
    #
    result = 'До ЗНО з фізики залишилось {} {}, а ти {}.'.format(days_physics, day_ukr[days_physics % 20], text)
    if text == '':
        warn_num = randint(0, warn_ukr.__len__())
        result = 'До ЗНО з фізики залишилось {} {}. {}.'.format(days_physics, day_ukr[days_physics % 20],
                                                                     warn_ukr[warn_num])
    query_result_ukr_physics = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Зворотній відлік фізика',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    id_ukr = get_sticker_id_with_text(bot, result)
    query_result_sticker_physics = InlineQueryResultCachedSticker(type='sticker', id=resId, sticker_file_id=id_ukr)
    resId += 1

    update.inline_query.answer(results=list([query_result_rus,
                                             query_result_ukr_math,
                                             query_result_ukr_ukr,
                                             query_result_ukr_eng,
                                             query_result_ukr_physics,
                                             query_result_sticker_math,
                                             query_result_sticker_ukr,
                                             query_result_sticker_eng,
                                             query_result_sticker_physics]),
                               cache_time=0,
                               is_personal=True)

    f = open('ids.cnf', 'w')
    f.write(str(resId))
    f.close()


zno_countdownbot = Bot(token=TOKEN)
updater = Updater(bot=zno_countdownbot)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(InlineQueryHandler(inline))

updater.start_polling()
updater.idle()
