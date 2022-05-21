from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from click import command
from model import *
from model.storage import StorageUser
import urllib.parse

class Flow():
    i: int
    run = False
    items = []

    def __init__(self, user: StorageUser,  res_id, run=False) -> None:
        self.user = user
        self.run = run
        # self.commands ={
        #     "помощь": res_id+0,
        #     "пожертвования": res_id+1,
        #     "пожертвования - список моих": res_id+101,
        #     "карточки": res_id+2,
        #     "запросы":res_id+3,
        #     "склад":res_id+4,
        #     "пользователь":res_id+5,
        # }
        
        self.commands ={
            "помощь": 0,
            "пожертвования": 1,
            "пожертвования - список моих": 101,
            "пожертвования - список всех": 102,
            "карточки": 2,
            "запросы":3,
            "склад":4,
            "пользователь":5,
        }

    def articles(self,mes: str):
        self.items.clear()
        self.ap(InlineQueryResultArticle(
            id=self.commands.get("помощь"),
            title=f'🔴 Это конструктор команд. Нажми на этот пункт для справки',
            input_message_content=InputTextMessageContent("/help"),
            ))
        if mes=="":
            self.build_start()
            return self.items
        if mes.lower() == "п":
            self.build_resources()
            return self.items
        return
               


        if mes.find("предложить в")==0:
            pass

    def build_start(self):
        self.ap(InlineQueryResultArticle(
        id=self.commands.get("пожертвования"),
        title=f'🔴 П - команды для пожертвований',
        input_message_content=InputTextMessageContent( \
                self.com_error_mes('пожертвования')),
        ))
        if self.user.prop.get('moderator')==1:
            self.ap(InlineQueryResultArticle(
            id=self.commands.get("карточки"),
            title=f'🔴 Н - команды для карточек нуждающихся ',
            input_message_content=InputTextMessageContent( \
                self.com_error_mes('карточки нуждающихся')),
            ))
            self.ap(InlineQueryResultArticle(
            id=self.commands.get("запросы"),
            title=f'🔴 З - команды для запросов ',
            input_message_content=InputTextMessageContent( \
                self.com_error_mes('запросы')),
            ))
            self.ap(InlineQueryResultArticle(
            id=self.commands.get("склад"),
            title=f'🔴 Х - команды для склада ',
            input_message_content=InputTextMessageContent( \
                self.com_error_mes('склад')),
            ))
        if self.user.prop.get('admin')==1:
            self.ap(InlineQueryResultArticle(
            id=self.commands.get("пользователь"),
            title=f'🔴 Ю - команды для управления пользователями ',
            input_message_content=InputTextMessageContent( \
                self.com_error_mes('пользователи')),
            ))
        return

    def build_resources(self):
        self.ap(InlineQueryResultArticle(
        id=self.commands.get("пожертвования - список моих"),
        title=f'📰 Пc - посмотреть мои пожертвования',
        input_message_content=InputTextMessageContent( \
                self.com_error_mes('пожертвования')),
        ))
        if self.user.prop.get('moderator')==1 or self.user.prop.get('admin')==1:
            self.ap(InlineQueryResultArticle(
            id=self.commands.get("пожертвования - список всех"),
            title=f'📰 Пc - посмотреть все пожертвования',
            input_message_content=InputTextMessageContent( \
                    self.com_error_mes('пожертвования')),
            ))
        return

    def ap(self, item:InlineQueryResultArticle):
        self.items.append(item)
        # self.i += 1

    def com_error_mes(self, command):
        return f'@{self.user.prop.get("name")} хотел(а) ввести команду `{command}`,' + \
                                ' но не ввел(а) команду полностью \n' + \
                                'Пожалуйста, воспользуйся справкой /help'


# print(Flow(StorageUser('468995539','taenfox'),123).articles(""))