import os
import enum
import json

import swordsmen
import tournament
import duel

class Phrases(enum.Enum):
    START="""Добро пожаловать в игру
"Турнир мастеров меча"\U00002694!

Для просмотра доступных команд используйте /help"""
    
    HELP="""Список доступных команд:

/show_classes - вывести список доступных классов мечников
/create_swordsman <имя> <класс> - создать нового мечника
/show_swordsman <имя> - вывести информацию о мечнике по его имени
/show_swordsmen - вывести список доступных мечников
/delete_swordsman <имя> - удалить мечника по имени
 
/create_tournament <число мечников> - организовать новый турнир с указанным числом участников
/add_swordsman <имя> - добавить нового участника по имени
/start_tournament - начать турнир
/save_tournament - сохранить текущий турнир
/load_tournament - загрузить последний сохраненный турнир
/start_duel - начать очередной поединок
/set_duel_view - сменить режим отображения поединка"""
    
    CLASS_LIST="Список доступных классов мечников:"+"\n\U00002022 ".join(swordsmen.get_classes_list())
    
    CREATE_SWORDSMAN_SUCCES="{0} {1} успешно создан"
    
    CREATE_SWORDSMAN_IS_EXISTS="{0} {1} уже существует"
    
    CREATE_SWORDSMAN_CLASS_NOT_EXISTS="Класс {0} не существует"
    
    CREATE_SWORDSMAN_FAIL="При создании {0} {1} произошла ошибка"
    
    DELETE_SWORDSMAN_SUCCESS="Мечник {0} успешно удален"
    
    DELETE_SWORDSMAN_NOT_EXISTS="Мечника {0} не существует"
    
    DELETE_SWORDSMAN_FAIL="Не удалось удалить мечника {0}"
    
    CREATE_TOURNAMENT_SUCCESS="Турнир из {0} участников успешно создан"
    
    CREATE_TOURNAMENT_WRONG_NUMBER="Число участников может быть только 2, 4, 8 или 16"
    
    ADD_SWORDSMAN_SUCCESS="Мечник {0} успешно заявлен как участник"
    
    ADD_SWORDSMAN_NOT_EXISTS="Мечника {0} не существует"
    
    ADD_SWORDSMAN_IS_EXISTS="Мечник {0} уже заявлен"
    
    ADD_SWORDSMAN_TOO_MANY="Турнир уже полностью укомплектован"
    
    START_TOURNAMENT_SUCCESS="""Начинаем турнир из {0} участников.
Чтобы просмотреть турнирную таблицу, используйте команду /show_table
Чтобы начать очередной поединок, используйте команду /start_duel"""
    
    START_TOURNAMENT_NOT_ENOUGH="Турнир не укомплектован. Не хватает {0} участника(-ов)."
    
    START_TOURNAMENT_NOT_CREATED="Турнир еще не организован (используйте /create_tournament)."
    
    SAVE_TOURNAMENT_SUCCESS="Текущий турнир успешно сохранен"
    
    LOAD_TOURNAMENT_SUCCESS="""Турнир из {0} участников успешно загружен.
Чтобы просмотреть турнирную таблицу, используйте команду /show_table
Чтобы начать очередной поединок, используйте команду /start_duel"""
    
    LOAD_TOURNAMENT_FAIL="Не удалось загрузить файл турнира"
    
    CURRENT_STAGE="Осталось поединков до окончания этапа: {0}."
    
    NEXT_STAGE="Этап {0} окончен. Переходим на этап {1}."
    
    FINAL_STAGE="Турнир окончен! Победитель турнира - {0}!"
    
    DUEL_VIEW="Режим отображения поединка: {0}"
    
class Scenes(enum.Enum):
    TITLE=enum.auto()
    STAGE=enum.auto()
    DUEL=enum.auto()
    RESULTS=enum.auto()

class GameManager:
    def __init__(self):
        self.swordsmen_dict=dict()
        self.current_scene=Scenes.TITLE
        self.update_swordsmen_dict()
        self.duel_detailed=False
        self.current_duelists=tuple()
        
    def create_swordsman(self,name,class_name):
        try:            
            names=list(map(lambda x: x.removesuffix(".json"),os.listdir("swordsmen")))
            if(name not in names):
                obj=swordsmen.create_swordsman(name,class_name)
                dict_to_write=obj.__dict__
                del dict_to_write["action"]
                with open(f"swordsmen\\{name}.json","w") as write_file:
                    json.dump(dict_to_write,write_file,indent=4)
                self.update_swordsmen_dict()
                return Phrases.CREATE_SWORDSMAN_SUCCES.value.format(class_name,name)
            else:
                return Phrases.CREATE_SWORDSMAN_IS_EXISTS.value.format(class_name,name)
        except TypeError:
            return Phrases.CREATE_SWORDSMAN_CLASS_NOT_EXISTS.value.format(class_name,name)
        except Exception:
            return Phrases.CREATE_SWORDSMAN_FAIL.value.format(class_name,name)
    
    def show_swordsmen(self):
        s="Список доступных мечников:"
        if(not len(self.swordsmen_dict)): s+="\nсписок пуст"
        else:
            for key in self.swordsmen_dict:
                s+=f"\n\U00002022 {self.swordsmen_dict[key].class_name} {key}"
        return s
    
    def delete_swordsman(self,name):
        try:
            names=list(map(lambda x: x.removesuffix(".json"),os.listdir("swordsmen")))
            if(name in names):
                os.remove(f"swordsmen\\{name}.json")
                self.update_swordsmen_dict()
                return Phrases.DELETE_SWORDSMAN_SUCCESS.value.format(name)
            else:
                return Phrases.DELETE_SWORDSMAN_NOT_EXISTS.value.format(name)
        except Exception:
            return Phrases.DELETE_SWORDSMAN_FAIL.value.format(name)
    
    def update_swordsmen_dict(self):
        self.swordsmen_dict.clear()
        files=os.listdir("swordsmen")
        data=dict()
        obj=None
        for v in files:
            with open(f"swordsmen\\{v}","r") as read_file:
                data=json.load(read_file)
            obj=swordsmen.create_swordsman(data["name"],data["class_name"])
            self.swordsmen_dict[v.removesuffix(".json")]=obj
    
    def create_tournament(self,contestant_count):
        try:
            self.tournament=tournament.Tournament(contestant_count)
            return Phrases.CREATE_TOURNAMENT_SUCCESS.value.format(contestant_count)
        except tournament.ContestantCountError:
            return Phrases.CREATE_TOURNAMENT_WRONG_NUMBER.value
    
    def add_swordsman(self,name):
        if name not in self.swordsmen_dict: return Phrases.ADD_SWORDSMAN_NOT_EXISTS.value.format(name)
        if name in self.tournament.contestants_dict: return Phrases.ADD_SWORDSMAN_IS_EXISTS.value.format(name)
        try:
            self.tournament.add_contestant(self.swordsmen_dict[name])
            return Phrases.ADD_SWORDSMAN_SUCCESS.value.format(name)
        except tournament.TooManyContestantsError:
            return Phrases.ADD_SWORDSMAN_TOO_MANY.value
        
    def start_tournament(self):
        try:
            self.tournament.assign_contestants()
            self.current_scene=Scenes.STAGE
            return Phrases.START_TOURNAMENT_SUCCESS.value.format(self.tournament.contestant_count)
        except tournament.NotEnoughContestantsError:
            return Phrases.START_TOURNAMENT_NOT_ENOUGH.value.format(self.tournament.contestant_count-len(self.tournament.contestants_dict))
        except AttributeError:
            return Phrases.START_TOURNAMENT_NOT_CREATED.value
        
    def save_tournament(self):
        with open("tournament.json","w") as write_file:
            json.dump(self.tournament.stages_dict,write_file,indent=4)
        return Phrases.SAVE_TOURNAMENT_SUCCESS.value
    
    def load_tournament(self):
        try:
            with open(f"tournament.json","r") as read_file:
                data=json.load(read_file)
            self.create_tournament(len(data["first"])*2)
            for v in data["first"]:
                respond=self.add_swordsman(v["pair"][0])
                if respond==Phrases.ADD_SWORDSMAN_NOT_EXISTS.value.format(v["pair"][0]):
                    return "При загрузке турнира возникла ошибка: "+respond
                respond=self.add_swordsman(v["pair"][1])
                if respond==Phrases.ADD_SWORDSMAN_NOT_EXISTS.value.format(v["pair"][1]):
                    return "При загрузке турнира возникла ошибка: "+respond
            self.tournament.stages_dict=data
            self.tournament.stage=len(list(data.keys()))-1
            self.current_scene=Scenes.STAGE
            return Phrases.LOAD_TOURNAMENT_SUCCESS.value.format(self.tournament.contestant_count)
        except Exception:
            return Phrases.LOAD_TOURNAMENT_FAIL.value
        
    
    def start_duel(self):
        pair=self.tournament.assign_duelists()
        self.current_duelists=(self.swordsmen_dict[pair["pair"][0]],self.swordsmen_dict[pair["pair"][1]])
        self.duel=duel.Duel(pair,self.current_duelists)
        return f"Начинается поединок между {self.duel.attacker.name} и {self.duel.defender.name}"
    
    def get_duelists_params(self):
        return f"{self.current_duelists[0].name}\n{self.current_duelists[0].get_current_params()}\n\n\
            {self.current_duelists[1].name}\n{self.current_duelists[1].get_current_params()}"
    
    def advance_stage(self):
        result=self.tournament.move_to_next_stage()
        if result[0]==1:
            return Phrases.NEXT_STAGE.value.format(result[1],result[1]+1)
        elif result[0]==2:
            self.current_scene=Scenes.TITLE
            self.tournament=None
            return Phrases.FINAL_STAGE.value.format(result[1])
        else:
            return Phrases.CURRENT_STAGE.value.format(result[1])
        
    def set_duel_view(self):
        self.duel_detailed=False if self.duel_detailed else True
        return Phrases.DUEL_VIEW.value.format("подробный" if self.duel_detailed else "по умолчанию")