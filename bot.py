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
import flow


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
async def inline_result(inline_query: InlineQuery):
    print("Новый запрос".center(60, "*"))
    print(inline_query)
    text = inline_query.query
    # input_content = InputTextMessageContent(text)
    # result_id: str = hashlib.md5(text.encode()).hexdigest()
    user = storage.StorageUser( \
        inline_query.from_user.id, \
        inline_query.from_user.username)
    
    await bot.answer_inline_query(inline_query.id, \
        results=flow.Flow(user, int(inline_query.id)).articles(text), \
        cache_time=0)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
