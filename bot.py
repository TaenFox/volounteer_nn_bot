from nis import match
import hashlib
import config
import logging
from model import item
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, \
    CallbackQuery

import db
from model import storage
import flow


# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.callback_query_handler()
async def run_command(query: CallbackQuery):
    data = flow.My_command()
    data.decompile(query.data)
    operator=storage.StorageUser(query.from_user.id, query.from_user.username)
    operator_id=operator.prop.get('id')
    is_admin = operator.prop.get('admin')
    is_moderator = operator.prop.get('moderator')


    #проверяем принадлежность кнопки для пользователя
    if int(query.from_user.id)!=data.auth:
        await bot.answer_callback_query(query.id, show_alert=True, text="Эта кнопка предназначена для другого пользователя")
        return

    #смотрим секцию
    if data.section == 'п':
        pass

# секции справочника наименований
    if data.section == 'нн':
        pass
    if data.section == 'нк':
        if is_admin!=True:
            await bot.answer_callback_query(query.id, show_alert=True, text="Для выполнения этой команды нужно быть администратором")
            return
        if data.context=='all':
            answer_text = 'Активны следующие категории:'
            cat:item.Category
            for cat in item.get_categories():
                cat_name = cat.prop.get("name")
                cat_id = cat.prop.get("id")
                len_id = 6
                if cat.prop.get('parent') == None:
                    cat_string = f'\n`{cat_id}``' + '-'*(len_id-len(str(cat_id))) + f'``{cat_name}`'
                else:
                    cat_string = f'\n`{cat_id}``' + '-'*(len_id-len(str(cat_id))+4) + f'``{cat_name}`'
                answer_text = answer_text + cat_string
            await bot.send_message(chat_id=query.from_user.id, parse_mode='Markdown', text=answer_text,)
            await bot.answer_callback_query(query.id) 
            return
        if data.context == 'new':
            new_cat_name = query.message.text
            obj_cat = item.Category(0)
            obj_cat.prop.update({'name':new_cat_name})
            obj_cat.update_data()
            answer_text = f'Категория {new_cat_name} добавлена\nid = {obj_cat.prop.get("id")}'
            await bot.answer_callback_query(query.id, show_alert=True, text=answer_text)

    if data.section == 'з':
        pass
    if data.section == 'х':
        pass

#секция пользователь
    if data.section[0] == 'ю':
        if is_admin!=True:
            await bot.answer_callback_query(query.id, show_alert=True, text="Для выполнения этой команды нужно быть администратором")
            return
        dest_user = storage.StorageUser(storage.get_tgid(data.destination),storage.get_tgname(data.destination))
        #показать всех
        if data.context == 'all':
            answer_text = 'Список пользователей:\n'
            for user in storage.get_users():
                len_name = len(user.prop.get('name'))
                len_space = 20 - len_name
                if len_space<1:
                    len_space=1
                if user.prop.get('admin')==True:
                    pic = '👮‍♀️'
                elif user.prop.get('moderator')==True:
                    pic = '👨‍💻'
                elif user.prop.get('banned')==True:
                    pic = '💔'
                else:
                    pic = '👤'
                answer_text = f"{answer_text}{pic} `@{user.prop.get('name')}``{'-'*len_space}``{user.prop.get('tgid')}`\n"
            await bot.send_message(
                chat_id=query.from_user.id,
                parse_mode='Markdown',
                text=answer_text,
                )
            await bot.answer_callback_query(query.id) 
            return
        #сделать админом
        if data.section == 'юа':
            dest_user.do_admin(operator_id)
        #сделать модератором
        if data.section == 'юм':
            dest_user.do_moderator(operator_id)
        #забанить пользователя
        if data.section == 'юб':
            dest_user.do_ban(operator_id)
        await bot.answer_callback_query(query.id, show_alert=True, text=dest_user.description_update())
        return
    
    await bot.answer_callback_query(query.id) 

@dp.message_handler()
async def echo(message: types.Message):
    # print(message.text)
    # user = {}
    # user.update({'id':message.from_user.id})
    # user.update({'name':message.from_user.username})
    # a = storage.StorageUser(user.get('id'), user.get('name'))
    # if message.text=='покажи все категории':
    #     list_cat = 'Список категорий:\n'
    #     for i in item.get_categories():
    #         list_cat = list_cat + "\n" + i.pub_name 
    #     await message.answer(list_cat)
    # if message.text=='добавить предложение':
    #     res = a.add_resource()
    # await message.answer(message.text)
    pass

@dp.inline_handler()
async def inline_result(inline_query: InlineQuery):
    print("Новый запрос".center(60, "_"))
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
