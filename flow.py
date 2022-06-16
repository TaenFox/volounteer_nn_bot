from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle, \
    InlineKeyboardMarkup, InlineKeyboardButton
from model import *
from model import storage
from model import item
from model.storage import StorageUser, StorageUser
import json, time

class Flow():
    i: int
    run = False
    items = []

    def __init__(self, user: StorageUser, run=False, data="") -> None:
        self.user = user.prop
        self.user_id = self.user.get('tgid')
        # self.run = run
        # self.data = My_command().decompile(data)

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

            "наименование":6,
            "наименование - добавить":600,
            "наименование - список всех":602,
            "наименование - заглушка для двоеточия":610,
            "наименование - заглушка для двоеточия2":611,
            # "наименование - удалить с заменой":603,
            "категория":7,            
            "категория - добавить":700,
            "категория - список всех": 702,
            # "категория - архивировать": 702
            "категория - заглушка для двоеточия":710,
            "категория - заглушка для двоеточия2":711,
        }

    def articles(self,mes: str):
        self.items.clear()
        self.ap(InlineQueryResultArticle(
            id=self.commands.get("помощь"),
            title=f'🔴 Это конструктор команд. Нажми на этот пункт для справки',
            input_message_content=InputTextMessageContent("/help"),
            ))
        if self.user.get("banned")==1:
            self.ap(InlineQueryResultArticle(
                id=0,
                title=f'💔 ты забанен',
                input_message_content=InputTextMessageContent('')))
            return
        if mes=="":
            self.build_start()

        if mes.lower().find('п') == 0:
            self.build_resources()
            
        if mes.lower().find('ю') == 0:
            self.build_users(mes)

        if mes.lower().find('н') == 0:
            self.build_items(mes)
        return self.items
               

    def build_start(self):
        arts = [
            #доступ                  код команды      текст                                                              текст ошибки
            [0,    self.commands.get("пожертвования"),"🔴 п - команды для пожертвований",             self.com_error_mes("пожертвования")],
            [1,    self.commands.get("карточки"),     "🔴 н - команды для карточек нуждающихся",      self.com_error_mes("карточки нуждающихся")],
            [1,    self.commands.get("запросы"),      "🔴 з - команды для запросов",                  self.com_error_mes("запросы")],
            [1,    self.commands.get("склад"),        "🔴 х - команды для склада",                    self.com_error_mes("склад")],
            [1,    self.commands.get("наименование"), "🔴 н - команды для справочника наименований",  self.com_error_mes("наименование")],
            [2,    self.commands.get("пользователь"), "🔴 ю - команды для управления пользователями ",self.com_error_mes("пользователи")]
        ]

        for art in arts:
            if art[0]==0: self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))

        if self.user.get('moderator')==1:
            for art in arts:
                if art[0]==1: self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))

        if self.user.get('admin')==1:
            for art in arts:
                if art[0]==2: self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))            
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
        if self.user.get('moderator')==1 or self.user.get('admin')==1:
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
        button_calback_data_get_all_users = My_command(
                        self.user_id,
                        'ю',
                        'all',
                        self.user.get('id')
                    ).compile()
        arts = [
#доступ                  код команды                                текст                                                          текст ответа                              этап      текст кнопки     данные кнопки
[2,    self.commands.get("пользователь - список всех"),             "📰 получить список пользователей",                           "Посмотреть список пользователей",        "ю",      "Показать",      button_calback_data_get_all_users],
[2,    self.commands.get("пользователь - забанить"),                "🔴 б - забанить/разбанить пользователя",  self.com_error_mes("бан/разбан пользователя"),               "ю",      None,            None],
[2,    self.commands.get("пользователь - сделать модератором"),     "🔴 м - дать/забрать права модератора",    self.com_error_mes("дать/забрать права модератора"),         "ю",      None,            None],
[2,    self.commands.get("пользователь - сделать админом"),         "🔴 а - дать/забрать права админа",        self.com_error_mes("дать/забрать права админа"),             "ю",      None,            None],
        ]
        if self.user.get('admin')==1:
            if mes=='ю':
                for art in arts:
                    if art[0]==2 and art[4]=="ю":
                        if art[5] != None:
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=art[5],callback_data=art[6]))))
                        else:
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))

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
                        if len(mes.split(":")[1])>0:
                            if mes.split(":")[1].isnumeric():
                                user_list = storage.get_users(id=mes.split(":")[1])
                            else:
                                user_list = storage.get_users(name=mes.split(":")[1])
                        else:
                            user_list = storage.get_users()
                        # if len(user_list)==0: return
                        mode={
                            'а': 'Записать/выписать в администраторы',
                            'м': 'Записать/выписать в модераторы',
                            'б': 'Забанить/разбанить',
                        }

                        i=-1
                        x=len(user_list)-1
                        obj_user: StorageUser
                        if x>45:
                            x=45
                        while i<x:
                            i+=1
                            obj_user = user_list[i]
                            user_id = obj_user.prop.get('id')
                            user_name = obj_user.prop.get('name')
                            button_calback_data = My_command(
                                    self.user_id,
                                    mes[:2],
                                    "",
                                    user_id
                                ).compile()
                            self.ap(InlineQueryResultArticle(
                            id=1000000000000000+user_id,
                            title=f"👤 {user_name} id={obj_user.prop.get('tgid')}",
                            input_message_content=InputTextMessageContent(obj_user.description_update()),
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                text=mode.get(mes[1]),
                                callback_data=button_calback_data
                                ))))
                    
    def build_items(self,mes:str):
        # "наименование":6,
        # "наименование - добавить":600,
        # "наименование - список всех":602,
        # "категория - добавить":700,
        # "категория - список всех": 702
        # "наименование - удалить с заменой":603,

        is_admin = self.user.get('admin')
        # is_moder = self.user.get('moderator')

        button_calback_data_get_all_items = My_command(self.user_id, 'нн', 'all', self.user.get('id')).compile()
        button_calback_data_new_items =     My_command(self.user_id, 'нн', 'new', 0).compile()
        button_calback_data_get_all_cats =  My_command(self.user_id, 'нк', 'all', self.user.get('id')).compile()
        button_calback_data_new_category =  My_command(self.user_id, 'нк', 'new', 0).compile()
        arts = [
#доступ                  код команды                                текст                                                          текст ответа                              этап      текст кнопки     данные кнопки
[2,    self.commands.get("наименование - список всех"),             "📰 Показать список всех наименований",                        "Показать все наименования",              "н",      "Показать",      button_calback_data_get_all_items],
[2,    self.commands.get("наименование - добавить"),                "🔴 н - добавить наименование",             self.com_error_mes("добавить наименование"),                 "н",      None,            None],
[2,    self.commands.get("категория"),                              "🔴 к - команды для категорий",             self.com_error_mes("категория"),                             "н",      None,            None],
[2,    self.commands.get("наименование - заглушка для двоеточия"),  "🔴 \":\" чтобы указать наименование", 
                                                                                                                self.com_error_mes("наименование - добавить"),                "нн",    None,            None],
[2,    self.commands.get("наименование - заглушка для двоеточия2"), "🔴 \":\" чтобы указать категорию", 
                                                                                                                self.com_error_mes("наименование - добавить"),                "нн2",   None,            None],
[2,    self.commands.get("категория - список всех"),                "📰 Показать список всех категорий",                           "Показать все категории",                 "нк",     "Показать",      button_calback_data_get_all_cats],
[2,    self.commands.get("категория - добавить"),                   "🔴 н - добавить категорию",                self.com_error_mes("категория - добавить"),                  "нк",     None,            None],
[2,    self.commands.get("категория - заглушка для двоеточия"),     "🔴 \":\" чтобы указать название категории", 
                                                                                                                self.com_error_mes("категория - добавить"),                  "нкн",     None,            None],
[2,    self.commands.get("категория - заглушка для двоеточия2"),    "🔴 \":\" чтобы указать название родительской категории", 
                                                                                                                self.com_error_mes("подкатегория - добавить"),               "нкн2",    None,            None],
        ]
        if is_admin==True:
            
            if mes=="н":
                for art in arts:
                    if art[0]==2 and art[4]=="н":
                        if art[5] != None:
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=art[5],callback_data=art[6]))))
                        else:
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))
            if mes.find('нн')==0:  # добавить наименование
                if mes == 'нн':
                    for art in arts:
                        if art[0]==2 and art[4]=="нн":
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))

                if len(mes)>2 and mes[2]==":":
                    if len(mes.split(":"))==2:
                        answer = mes.split(':')[1]
                        print(answer)
                        if answer=='': 
                            answer='Начни вводить наименования'
                            self.ap(InlineQueryResultArticle(
                            id=str(self.commands.get("наименование - добавить"))+str(round(time.time()*100)),
                            title=f"🔴 {answer}",
                            input_message_content=InputTextMessageContent( \
                                self.com_error_mes('наименование - добавить')),))
                        else:
                            for art in arts:
                                if art[0]==2 and art[4]=="нн2":
                                    self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))
                            self.ap(InlineQueryResultArticle(
                            id=str(self.commands.get("наименование - добавить"))+str(round(time.time()*100)),
                            title=f"🔴 добавить {answer}",
                            input_message_content=InputTextMessageContent(answer),
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                text='Добавить наименование',
                                callback_data=button_calback_data_new_category
                                ))))

                    if len(mes.split(":"))==3:
                        for art in arts:
                            if art[0]==2 and art[4]=="нн2":
                                self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))
                        self.ap(InlineQueryResultArticle(
                        id=str(self.commands.get("наименование - добавить"))+str(round(time.time()*100)),
                        title=f"🔴 укажи id категории для \'{answer}\'",
                        input_message_content=InputTextMessageContent( \
                            self.com_error_mes('наименование - добавить')),))

                        par_cat = item.get_categories(name = mes.split(":")[2])
                        i = 0
                        x=len(par_cat)-1
                        obj_cat: item.Category
                        if x>45:
                            x=45
                        while i<x:
                            i+=1
                            obj_cat = par_cat[i]
                            self.ap(InlineQueryResultArticle(
                            id=str(self.commands.get("категория - добавить"))+str((time.time()%1))[2:],
                            title=f"➕ добавить наименование {answer} в категорию {obj_cat.prop.get('name')}",
                            input_message_content=InputTextMessageContent(answer),
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                text='Добавить наименование',
                                callback_data=button_calback_data_new_items
                                ))))

            if mes=='нк':   #наименование - категория
                for art in arts:
                    if art[0]==2 and art[4]=="нк":
                        if art[5] != None:
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=art[5],callback_data=art[6]))))
                        else:
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))

            if mes.find('нкн')==0:  # добавить категорию
                if mes == 'нкн':
                    for art in arts:
                        if art[0]==2 and art[4]=="нкн":
                            self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))

                if len(mes)>3 and mes[3]==":":
                    if len(mes.split(":"))==2:
                        answer = mes.split(':')[1]
                        print(answer)
                        if answer=='': 
                            answer='Начни вводить название категории'
                            self.ap(InlineQueryResultArticle(
                            id=str(self.commands.get("категория - добавить"))+str(round(time.time()*100)),
                            title=f"🔴 {answer}",
                            input_message_content=InputTextMessageContent( \
                                self.com_error_mes('категория - добавить')),))
                        else:
                            for art in arts:
                                if art[0]==2 and art[4]=="нкн2":
                                    self.ap(InlineQueryResultArticle(id=art[1], title=art[2],input_message_content=InputTextMessageContent(art[3]),))
                            self.ap(InlineQueryResultArticle(
                            id=str(self.commands.get("категория - добавить"))+str(round(time.time()*100)),
                            title=f"➕ добавить категорию {answer}",
                            input_message_content=InputTextMessageContent(answer),
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                text='Добавить категорию',
                                callback_data=button_calback_data_new_category
                                ))))
                    if len(mes.split(":"))==3:
                        answer = mes.split(':')[1]
                        print(answer)
                        if answer=='': 
                            answer='Начни вводить название категории'
                            self.ap(InlineQueryResultArticle(
                            id=str(self.commands.get("категория - добавить"))+str(round(time.time()*100)),
                            title=f"🔴 {answer}",
                            input_message_content=InputTextMessageContent( \
                                self.com_error_mes('категория - добавить')),))
                        else:
                            par_cat = item.get_categories(name = mes.split(":")[2])
                            i = 0
                            x=len(par_cat)-1
                            obj_cat: item.Category
                            if x>45:
                                x=45
                            while i<x:
                                i+=1
                                obj_cat = par_cat[i]
                                button_calback_data_new_sub_category = My_command(
                                    self.user_id,
                                    "нк",
                                    "new_sub",
                                    obj_cat.id
                                ).compile()
                                self.ap(InlineQueryResultArticle(
                                id=str(self.commands.get("категория - добавить"))+str((time.time()%1))[2:],
                                title=f"➕ добавить категорию {answer} в категорию {obj_cat.prop.get('name')}",
                                input_message_content=InputTextMessageContent(answer),
                                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                    text='Добавить подкатегорию',
                                    callback_data=button_calback_data_new_sub_category
                                    ))))

    def build_add_resource(self, mes):
        pass

    def ap(self, item:InlineQueryResultArticle):
        if self.run== False:
            print(item)
            self.items.append(item)

    def com_error_mes(self, command):
        return f'@{self.user.get("name")} хотел(а) ввести команду `{command}`,' + \
                                ' но не ввел(а) команду полностью \n' + \
                                'Пожалуйста, воспользуйся справкой /help'

class My_command():
    auth = ""
    section = ""
    context = ""
    destination = ""
    def __init__(self, auth="", section="", context="", destination="") -> None:
        self.auth = auth
        self.section = section
        self.context = context
        self.destination = destination
        
    def compile(self):
        data = {
            'a':self.auth,
            's':self.section,
            'c':self.context,
            'd':self.destination
        }
        return json.dumps(data)
    
    def decompile(self, data):
        array_data = {}
        array_data = json.loads(data)
        try:
            if array_data.get('a') is None or \
            array_data.get('s') is None or \
            array_data.get('c') is None or \
            array_data.get('d') is None:
                raise Exception()
            self.auth = int(array_data.get('a'))
            self.section = array_data.get('s')
            self.context = array_data.get('c')
            self.destination = int(array_data.get('d'))
        except:
            print(f"Отсутствует атрибут команды в строке {data}\nТребуются: \n\
    - 'a' - auth\n\
    - 's' - section\n\
    - 'c' - context\n\
    - 'd' - destination\n")
