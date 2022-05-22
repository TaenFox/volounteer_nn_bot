from ctypes.wintypes import PINT
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, \
    InlineKeyboardMarkup, InlineKeyboardButton
from click import command
from psutil import users
from model import *
from model import storage
from model.storage import StorageUser
import urllib.parse

class Flow():
    i: int
    run = False
    items = []

    def __init__(self, user: StorageUser,  res_id, run=False) -> None:
        self.user = user
        self.run = run

        self.commands ={
            "помощь": 0,
            "пожертвования": 1,
            "пожертвования - добавить": 100,
            "пожертвования - список моих": 101,
            "пожертвования - список всех": 102,

            "карточки": 2,
            "карточки - добавить": 200,
            "карточки - посмотрить мои": 201,
            "карточки - посмотреть все": 202,

            "запросы":3,
            "запросы - добавить":300,
            "запросы - посмотреть все":302,
            "запросы - посмотреть по карточке":303,

            "склад":4,
            "склад - добавить склад":400,
            "склад - список складов":402,
            "склад - закрыть склад":405,

            "пользователь":5,
            "пользователь - список всех":502,
            "пользователь - забанить":505,
            "пользователь - сделать модератором":508,
            "пользователь - сделать админом":509,
            "пользователь - заглушка для двоеточия":510,
            "пользователь - заглушка для указания пользователя":511,
        }

    def articles(self,mes: str):
        self.items.clear()
        self.ap(InlineQueryResultArticle(
            id=self.commands.get("помощь"),
            title=f'🔴 Это конструктор команд. Нажми на этот пункт для справки',
            input_message_content=InputTextMessageContent("/help"),
            ))
        if self.user.prop.get("banned")==1:
            self.ap(InlineQueryResultArticle(
                id=0,
                title=f'💔 ты забанен',
                input_message_content=InputTextMessageContent('')))
            return
        if mes=="":
            self.build_start()

        if mes.lower() == "п":
            self.build_resources()
            
        if mes.lower().find('ю') == 0:
            self.build_users(mes)
        return self.items
               

    def build_start(self):
        self.ap(InlineQueryResultArticle(
            id=self.commands.get("пожертвования"),
            title=f'🔴 п - команды для пожертвований',
            input_message_content=InputTextMessageContent( \
                    self.com_error_mes('пожертвования')),))
        if self.user.prop.get('moderator')==1:
            self.ap(InlineQueryResultArticle(
                id=self.commands.get("карточки"),
                title=f'🔴 н - команды для карточек нуждающихся ',
                input_message_content=InputTextMessageContent( \
                    self.com_error_mes('карточки нуждающихся')),))
            self.ap(InlineQueryResultArticle(
                id=self.commands.get("запросы"),
                title=f'🔴 з - команды для запросов ',
                input_message_content=InputTextMessageContent( \
                    self.com_error_mes('запросы')),))
            self.ap(InlineQueryResultArticle(
                id=self.commands.get("склад"),
                title=f'🔴 х - команды для склада ',
                input_message_content=InputTextMessageContent( \
                    self.com_error_mes('склад')),))
        if self.user.prop.get('admin')==1:
            self.ap(InlineQueryResultArticle(
                id=self.commands.get("пользователь"),
                title=f'🔴 ю - команды для управления пользователями ',
                input_message_content=InputTextMessageContent( \
                    self.com_error_mes('пользователи')),))
        return

    def build_resources(self):
        self.ap(InlineQueryResultArticle(
            id=self.commands.get("пожертвования - добавить"),
            title=f'🔴 н - добавить пожертвование',
            input_message_content=InputTextMessageContent( \
                self.com_error_mes('пожертвования')),))
        self.ap(InlineQueryResultArticle(
            id=self.commands.get("пожертвования - список моих"),
            title=f'📃 список моих пожертвований',
            input_message_content=InputTextMessageContent( \
                self.com_error_mes('пожертвования')),))
        if self.user.prop.get('moderator')==1 or self.user.prop.get('admin')==1:
            self.ap(InlineQueryResultArticle(
                id=self.commands.get("пожертвования - список всех"),
                title=f'📰 посмотреть все пожертвования',
                input_message_content=InputTextMessageContent("посмотреть все пожертвования"),
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Показать',callback_data='test'))))
        return

    def build_users(self, mes:str):
        # "пользователь - список всех":502,
        # "пользователь - забанить":505,
        # "пользователь - сделать модератором":508,
        # "пользователь - сделать админом":509,
        # "пользователь - заглушка для двоеточия":510,
        # "пользователь - заглушка для указания пользователя":511,

        if self.user.prop.get('admin')==1:
            if mes=='ю':
                self.ap(InlineQueryResultArticle(
                    id=self.commands.get("пользователь - список всех"),
                    title=f'📰 получить список пользователей',
                    input_message_content=InputTextMessageContent("посмотреть список пользователей"),
                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                        text='Показать',
                        callback_data='test'))))
                self.ap(InlineQueryResultArticle(
                    id=self.commands.get("пользователь - забанить"),
                    title=f'🔴 б - забанить/разбанить пользователя',
                    input_message_content=InputTextMessageContent(\
                        self.com_error_mes('бан/разбан пользователя')),))
                self.ap(InlineQueryResultArticle(
                    id=self.commands.get("пользователь - сделать модератором"),
                    title=f'🔴 м - дать/забрать права модератора',
                    input_message_content=InputTextMessageContent(\
                        self.com_error_mes('дать/забрать права модератора')),))            
                self.ap(InlineQueryResultArticle(
                    id=self.commands.get("пользователь - сделать админом"),
                    title=f'🔴 а - дать/забрать права админа',
                    input_message_content=InputTextMessageContent(\
                        self.com_error_mes('дать/забрать права админа')),))
            if mes.find('юб')==0 or mes.find('юм')==0 or mes.find('юа')==0:
                if len(mes)==2:
                    self.ap(InlineQueryResultArticle(
                        id=self.commands.get("пользователь - заглушка для двоеточия"),
                        title=f'🔴 напиши ":" (двоеточие) чтобы указать пользователя',
                        input_message_content=InputTextMessageContent(\
                            self.com_error_mes('указать пользователя')),))
                    return
                if mes[2]==":":
                    self.ap(InlineQueryResultArticle(
                        id=self.commands.get("пользователь - заглушка для указания пользователя"),
                        title=f'🔴 Укажи id пользователя из подсказки и нажми на предлагаемый результат',
                        input_message_content=InputTextMessageContent(\
                            self.com_error_mes('указать пользователя')),))
                    if len(mes.split(":"))==2:
                        print(f'Длина строки после: {len(mes.split(":")[1])}, числовая?: {mes.split(":")[1].isnumeric()}')
                        if len(mes.split(":")[1])>0:
                            if mes.split(":")[1].isnumeric():
                                user_list = storage.get_users(id=mes.split(":")[1])
                            else:
                                user_list = storage.get_users(name=mes.split(":")[1])
                        else:
                            user_list = storage.get_users()
                        # if len(user_list)==0: return
                        i=-1
                        x=len(user_list)-1
                        if x>45:
                            x=45
                        while i<x:
                            i+=1
                            user_id = user_list[i][0]
                            user_name = user_list[i][1]
                            self.ap(InlineQueryResultArticle(
                            id=1000000000000000+user_id,
                            title=f"👤 {user_name} id={user_id}",
                            input_message_content=InputTextMessageContent(f"пользователь {user_name}"),
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                text='Показать',
                                callback_data='test'))))
                    
    def build_add_resource(self, mes):
        pass

    def ap(self, item:InlineQueryResultArticle):
        print(item)
        self.items.append(item)

    def com_error_mes(self, command):
        return f'@{self.user.prop.get("name")} хотел(а) ввести команду `{command}`,' + \
                                ' но не ввел(а) команду полностью \n' + \
                                'Пожалуйста, воспользуйся справкой /help'
