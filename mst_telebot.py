import time
import os
import telebot

from game_manager import GameManager,Phrases,Scenes
from controller import Controller
from swordsmen import Actions

gm=GameManager()

token_bot = os.getenv("TOKEN")
bot = telebot.TeleBot(token_bot)

commands = [
    telebot.types.BotCommand("start", "Приветствие"),
    telebot.types.BotCommand("help", "Доступные команды")
]

markup = telebot.types.InlineKeyboardMarkup()
df_btn = telebot.types.InlineKeyboardButton("", callback_data='df_btn')
dt_btn = telebot.types.InlineKeyboardButton("", callback_data='dt_btn')
markup.add(df_btn, dt_btn)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,Phrases.START.value)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,Phrases.HELP.value)
    
@bot.message_handler(commands=["show_classes"])
def show_classes(message):
    bot.send_message(message.chat.id,Phrases.CLASS_LIST.value)
    
@bot.message_handler(commands=["create_swordsman"])
def create_swordsman(message):
    try:
        _, name, class_name = message.text.split(maxsplit=2)
        bot.send_message(message.chat.id,gm.create_swordsman(name,class_name))
    except ValueError:
        bot.send_message(message.chat.id,"Введите <имя> и <класс>. Пример:\n/create_swordsman John Мечник Берсерк")    

@bot.message_handler(commands=["show_swordsmen"])
def show_swordsmen(message):
    bot.send_message(message.chat.id,gm.show_swordsmen())
    
@bot.message_handler(commands=["show_swordsman"])
def show_swordsman(message):    
    try:
        _, name = message.text.split(maxsplit=1)
        bot.send_message(message.chat.id,gm.swordsmen_dict[name])
    except ValueError:
        bot.send_message(message.chat.id,"Введите <имя>. Пример:\n/show_swordsman John")
    except KeyError:
        bot.send_message(message.chat.id,f"Мечника {name} не существует")

@bot.message_handler(commands=["delete_swordsman"])
def delete_swordsman(message):
    try:
        _, name = message.text.split(maxsplit=1)
        bot.send_message(message.chat.id,gm.delete_swordsman(name)) 
    except ValueError:
        bot.send_message(message.chat.id,"Введите <имя>. Пример:\n/delete_swordsman John")
        
@bot.message_handler(commands=["create_tournament"])
def create_tournament(message):
    try:
        _, count = message.text.split(maxsplit=1)
        count=int(count)
        bot.send_message(message.chat.id,gm.create_tournament(count)) 
    except Exception:
        bot.send_message(message.chat.id,"Введите <число мечников>. Пример:\n/create_tournament 8")
        
@bot.message_handler(commands=["add_swordsman"])
def add_swordsman(message):
    try:
        _, name = message.text.split(maxsplit=1)
        bot.send_message(message.chat.id,gm.add_swordsman(name)) 
    except ValueError:
        bot.send_message(message.chat.id,"Введите <имя>. Пример:\n/add_swordsman John")

@bot.message_handler(commands=["start_tournament"])
def start_tournament(message):
    if gm.current_scene!=Scenes.TITLE:
        bot.send_message(message.chat.id,"Турнир уже стартовал")
    else:
        bot.send_message(message.chat.id,gm.start_tournament())
        
@bot.message_handler(commands=["show_table"])
def show_table(message):
    if gm.current_scene!=Scenes.STAGE:
        bot.send_message(message.chat.id,"Турнир еще не начался (используйте /start_tournament)")
    else:
        bot.send_photo(message.chat.id,photo=gm.tournament.get_table_image())
        
@bot.message_handler(commands=["save_tournament"])
def save_tournament(message):
    if gm.current_scene!=Scenes.STAGE:
        bot.send_message(message.chat.id,"Турнир еще не начался (используйте /start_tournament)")
    else:
        bot.send_message(message.chat.id,gm.save_tournament())

@bot.message_handler(commands=["load_tournament"])
def load_tournament(message):
    bot.send_message(message.chat.id,gm.load_tournament())

@bot.message_handler(commands=["start_duel"])
def start_duel(message):
    if gm.current_scene!=Scenes.STAGE:
        bot.send_message(message.chat.id,"Турнир еще не организован")
    else:
        msg=bot.send_message(message.chat.id,gm.start_duel())
        time.sleep(3)
        if gm.duel_detailed:
            msg_text=gm.get_duelists_params()+"\n\n"+gm.duel.first_move()
            bot.edit_message_text(msg_text, chat_id=msg.chat.id, message_id=msg.id)
            time.sleep(3)
            while(gm.duel.pair["winner"]==""):
                controller=Controller(gm.duel.attacker,gm.duel.defender)
                is_moving=True
                while(is_moving):
                    actions=controller.make_move()
                    msg_text=gm.get_duelists_params()+"\n\n"+gm.duel.make_attacker_move(actions[0])+gm.duel.make_defender_move(actions[1])
                    bot.edit_message_text(msg_text, chat_id=msg.chat.id, message_id=msg.id)
                    time.sleep(2)
                    msg_text=gm.get_duelists_params()+"\n\n"+gm.duel.execute_all_actions()
                    bot.edit_message_text(msg_text, chat_id=msg.chat.id, message_id=msg.id)
                    time.sleep(2)
                    if actions[0]==Actions.PASS: is_moving=False
                msg_text=gm.get_duelists_params()+"\n\n"+gm.duel.pass_move()
                bot.edit_message_text(msg_text, chat_id=msg.chat.id, message_id=msg.id)
                time.sleep(3)
        else:
            while(gm.duel.pair["winner"]==""):
                controller=Controller(gm.duel.attacker,gm.duel.defender)
                is_moving=True
                while(is_moving):
                    actions=controller.make_move()
                    gm.duel.make_attacker_move(actions[0])
                    gm.duel.make_defender_move(actions[1])
                    gm.duel.execute_all_actions()
                    if actions[0]==Actions.PASS: is_moving=False
                gm.duel.pass_move()
            bot.send_message(message.chat.id,gm.duel.show_summary())              
        bot.send_message(message.chat.id,gm.advance_stage())
        
@bot.message_handler(commands=["set_duel_view"])
def set_duel_view(message):
    df_btn_txt="По умолчанию"
    dt_btn_txt="Подробный"
    if gm.duel_detailed: dt_btn_txt+=" \U00002705"
    else: df_btn_txt+=" \U00002705"
    df_btn.text=df_btn_txt
    dt_btn.text=dt_btn_txt
    bot.send_message(message.chat.id,"Выберите режим отображения поединка",reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'df_btn':
        gm.duel_detailed=False
        df_btn.text="По умолчанию \U00002705"
        dt_btn.text="Подробный"
        bot.edit_message_text('Выбран режим отображения: по умолчанию', chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)
    elif call.data == 'dt_btn':
        gm.duel_detailed=True
        df_btn.text="По умолчанию"
        dt_btn.text="Подробный \U00002705"
        bot.edit_message_text('Выбран режим отображения: подробный', chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)

bot.set_my_commands(commands)

bot.infinity_polling(skip_pending=True)