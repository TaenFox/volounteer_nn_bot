from nis import match
import hashlib
import config
import logging
from model import item
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

import db
from model import storage


# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

#echo
@dp.message_handler()
async def echo(message: types.Message):
    print(message.text)
    user = {}
    user.update({'id':message.from_user.id})
    user.update({'name':message.from_user.username})
    a = storage.StorageUser(user.get('id'), user.get('name'))
    if message.text=='покажи все категории':
        list_cat = 'Список категорий:\n'
        for i in item.get_categories():
            list_cat = list_cat + "\n" + i.pub_name 
        await message.answer(list_cat)
    # if message.text=='добавить предложение':
    #     res = a.add_resource()
    # await message.answer(message.text)

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):

    text = inline_query.query or 'echo'
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    items = []
    if text.find("предложить в")==0:
        item = InlineQueryResultArticle(
            id=1,
            title=f'Предложить в вещи',
            input_message_content=InputTextMessageContent('Предложить в вещи'),
        )
        items.append(item)
        item = InlineQueryResultArticle(
            id=2,
            title=f'Предложить в услуги',
            input_message_content=InputTextMessageContent('Предложить в услуги'),
        )
        items.append(item)

    else:
        item = InlineQueryResultArticle(
            id=result_id,
            title=f'Result {text!r}',
            input_message_content=input_content,
        )
        items.append(item)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
