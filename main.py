# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import Updater
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import InlineQueryResultDocument
from telegram import InlineQueryResultCachedSticker
from telegram import Bot
from datetime import date
from random import randint
from PIL import Image, ImageDraw, ImageFont


# bearImage = Image.open('./bb.webp')
CHAT_ID_ME = 205436582


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
ZNO_DATE = date.fromisoformat("2019-05-21")


def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
    update.message.reply_text('chat id: {}\nuid: {}'.format(update.message.chat.id, update.message.from_user.id))


def inline(bot, update):
    global resId
    # global bearImage
    delta = ZNO_DATE - date.today()
    days = delta.days
    day_rus = list(['дней', 'день', 'дня', 'дня', 'дня', 'дней', 'дней', 'дней', 'дней', 'дней', 'дней'])
    day_eng = list()
    day_ukr = list(['днів', 'день', 'дні', 'дні', 'дні', 'днів', 'днів', 'днів', 'днів', 'днів'])

    warn_rus = list(['Берегись', 'Осторожнее', 'Спасайся', 'Беги', 'Учись', 'Пора'])
    warn_ukr = list(['Тікай у село', 'Обережніше', 'Рятуйся', 'Ну ЗНУ це теж ЗВО', 'Починай готуватися', 'Готуй бабки',
                     'Солдат. Звучить не так і погано', 'Батько тебе породив, він тебе і вб\'є'])

    text = update.inline_query.query
    lang_code = update.inline_query.from_user.language_code

    result = 'До ЗНО осталось {} {}, а ты {}.'.format(days, day_rus[days % 10], text)

    if text == '':
        warn_num = randint(0, warn_rus.__len__())
        result = 'До ЗНО осталось {} {}. {}.'.format(days, day_rus[days % 10], warn_rus[warn_num])
    # print(text)

    # result += str(resId)
    queryResultRus = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Countdown Russian',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    result = 'До ЗНО залишилось {} {}, а ти {}.'.format(days, day_ukr[days % 10], text)
    if text == '':
        warn_num = randint(0, warn_ukr.__len__())
        result = 'До ЗНО залишилось {} {}. {}.'.format(days, day_ukr[days % 10], warn_ukr[warn_num])
        # print(result)

    # result += str(resId)
    queryResultUkr = InlineQueryResultArticle(
        id='{}'.format(resId),
        title='Countdown Ukrainian',
        input_message_content=InputTextMessageContent(
            message_text=result
        )
    )
    resId += 1

    img = Image.open('bear.webp')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('impact.ttf', size=100)

    LINE_MAX_LENGTH = 21
    res_text = ''
    wrap_num_a = 0
    wrap_num_b = 0
    while wrap_num_a + LINE_MAX_LENGTH < result.__len__():
        for i in range(wrap_num_a, min(wrap_num_a + LINE_MAX_LENGTH, result.__len__())):
            if result[i] == ' ':
                wrap_num_a = i + 1
            elif result[i] == '.':
                wrap_num_a = i
            # print(wrap_num_a)
        res_text += result[wrap_num_b:wrap_num_a] + '\n'
        wrap_num_b = wrap_num_a
    res_text += result[wrap_num_b:]

    draw.text((50, 20), font=font, text=res_text, fill=(90 + randint(0, 166), 60 + randint(0, 196),
                                                        90 + randint(10, 20), 200))
    img.save('bb.webp')
    # img.close()
    doc = open('bb.webp', 'rb')
    message = bot.send_document(chat_id=CHAT_ID_ME, document=doc)

    # query_result_document_sticker = InlineQueryResultDocument()
    query_result_sticker = InlineQueryResultCachedSticker(type='sticker', id=resId, sticker_file_id=message.sticker.file_id)
    resId += 1

    # print(update.inline_query.from_user)
    update.inline_query.answer(results=list([queryResultRus, queryResultUkr, query_result_sticker]),
                               cache_time=0,
                               is_personal=True)

    f = open('ids.cnf', 'w')
    f.write(str(resId))
    f.close()


bot = Bot(token='token')
updater = Updater(bot=bot)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(InlineQueryHandler(inline))

updater.start_polling()
updater.idle()
