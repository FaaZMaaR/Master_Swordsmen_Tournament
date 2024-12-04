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
        bot.send_message(message.chat.id,gm.start_duel())
        time.sleep(1)
        bot.send_message(message.chat.id,gm.duel.first_move())
        time.sleep(3)
        while(gm.duel.pair["winner"]==""):
            controller=Controller(gm.duel.attacker,gm.duel.defender)
            is_moving=True
            while(is_moving):
                actions=controller.make_move()
                bot.send_message(message.chat.id,gm.duel.make_attacker_move(actions[0])+gm.duel.make_defender_move(actions[1]))
                time.sleep(1)
                bot.send_message(message.chat.id,gm.duel.execute_all_actions())
                time.sleep(1)
                if actions[0]==Actions.PASS: is_moving=False
            bot.send_message(message.chat.id,gm.duel.pass_move())
            time.sleep(3)
        bot.send_message(message.chat.id,gm.advance_stage())

bot.set_my_commands(commands)

bot.infinity_polling(skip_pending=True)