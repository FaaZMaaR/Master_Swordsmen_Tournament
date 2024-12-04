import random
import enum

class SwordsmenClasses(enum.Enum):    
    DEFAULT=""
    BERSERK="Мечник Берсерк"
    FIRE="Мечник Огня"
    FROST="Мечник Мороза"
    SHOCK="Мечник Молнии"
    ASSASSIN="Мечник Убийца"
    PALADIN="Мечник Паладин"
    SORCERER="Мечник Колдун"
    
class Actions(enum.Enum):
    PASS=enum.auto()
    ATTACK=enum.auto()
    SPECIAL=enum.auto()
    HEAL=enum.auto()
    BLOCK=enum.auto()
    DODGE=enum.auto()
    COUNTER=enum.auto()

class Swordsman:
    def __init__(self,name,class_name=SwordsmenClasses.DEFAULT.value,attributes=None,skills=None,resistance=None):
        self.name=name
        self.class_name=class_name
        
        self.attributes={"health":100,"initiative":10,"skill":10,"armor":100} if attributes==None else attributes
        self.skills={"attacking":80,"defence":20,"dodging":20,"mastery":5,"healing":30} if skills==None else skills
        self.resistance={"heat":5,"cold":5,"shock":5,"poison":5,"curse":5} if resistance==None else resistance
        self.recovering={"ap":3,"sp":2}     
        
        self.reset_changing_params()
        
        self.is_attacking=False
        self.action=Actions.PASS
    
    def attack(self,block,arp):
        self.changing_params["ap"]-=3
        attack=self.skills["attacking"]
        hp_dmg=0
        arp_dmg=0
        if self.compare_attributes(attack,block):
            attack=random.randrange(attack//2,attack+1)
        else:
            return (hp_dmg,arp_dmg)
        if arp<attack:
            hp_dmg=attack-arp
            attack-=hp_dmg
        arp_dmg=random.randrange(attack+1)
        return (hp_dmg,arp_dmg)
    
    def block(self):
        self.changing_params["ap"]-=1
        return self.skills["defence"]
    
    def dodge(self):
        pass
    
    def counter(self):
        pass
    
    def do_special(self):
        pass
    
    def do_no_dodging_special(self):
        pass    
    
    def heal(self):        
        self.changing_params["sp"]-=4
        hp_incr=random.randrange(1,self.skills["healing"]+1)
        bleed_decr=random.randrange(1,self.skills["healing"]+1) if self.changing_params["bleeding"]>0 else 0
        self.changing_params["hp"]+=hp_incr
        if(self.changing_params["hp"]>self.attributes["health"]): self.changing_params["hp"]=self.attributes["health"]
        self.changing_params["bleeding"]-=bleed_decr
        if(self.changing_params["bleeding"]<0): self.changing_params["bleeding"]=0
        return (hp_incr,bleed_decr)             
    
    def skip(self):
        pass
    
    def reset_changing_params(self):
        self.changing_params={"hp":self.attributes["health"],
                              "ap":self.attributes["initiative"],
                              "sp":self.attributes["skill"],
                              "arp":self.attributes["armor"],
                              "fire_dmg":0,
                              "frost_dmg":0,
                              "shock_dmg":0,
                              "poison_dmg":0,
                              "bleeding":0}
        
    def recover(self):
        self.changing_params["hp"]-=self.changing_params["fire_dmg"]
        self.changing_params["ap"]-=self.changing_params["frost_dmg"]
        if self.changing_params["ap"]<0: self.changing_params["ap"]=0
        self.changing_params["sp"]-=self.changing_params["shock_dmg"]
        if self.changing_params["sp"]<0: self.changing_params["sp"]=0
        self.changing_params["hp"]-=self.changing_params["poison_dmg"]
        self.changing_params["hp"]-=self.changing_params["bleeding"]
        
        self.changing_params["fire_dmg"]-=self.resistance["heat"]
        if self.changing_params["fire_dmg"]<0: self.changing_params["fire_dmg"]=0
        self.changing_params["frost_dmg"]-=self.resistance["cold"]
        if self.changing_params["frost_dmg"]<0: self.changing_params["frost_dmg"]=0
        self.changing_params["shock_dmg"]-=self.resistance["shock"]
        if self.changing_params["shock_dmg"]<0: self.changing_params["shock_dmg"]=0
        self.changing_params["poison_dmg"]-=self.resistance["poison"]
        if self.changing_params["poison_dmg"]<0: self.changing_params["poison_dmg"]=0
             
        self.changing_params["ap"]+=self.recovering["ap"]
        if self.changing_params["ap"]>self.attributes["initiative"]: self.changing_params["ap"]=self.attributes["initiative"]
        self.changing_params["sp"]+=self.recovering["sp"]
        if self.changing_params["sp"]>self.attributes["skill"]: self.changing_params["sp"]=self.attributes["skill"]
    
    def __str__(self):
        return f"{self.name}, {self.class_name}\
            \n\nЗдоровье: {self.attributes["health"]}\nБроня: {self.attributes["armor"]}\
            \nИнициатива: {self.attributes["initiative"]}\nУмение: {self.attributes["skill"]}\
            \n\nАтака: {self.skills["attacking"]}\nЗащита: {self.skills["defence"]}\nУклонение: {self.skills["dodging"]}\
            \nМастерство: {self.skills["mastery"]}\nЛечение: {self.skills["healing"]}\
            \n\nСопротивление:\
            \n- огню: {self.resistance["heat"]}\n- морозу: {self.resistance["cold"]}\n- электричеству: {self.resistance["shock"]}\
            \n- яду: {self.resistance["poison"]}\n- проклятию: {self.resistance["curse"]}\
            \n\nВосстановление:\
            \n- очков действия: {self.recovering["ap"]}\n- очков умения: {self.recovering["sp"]}"
    
    def get_current_params(self):
        return f"Параметры:\nож: {self.changing_params["hp"]}/{self.attributes["health"]}\nод: {self.changing_params["ap"]}/{self.attributes["initiative"]}\
            \nоу: {self.changing_params["sp"]}/{self.attributes["skill"]}\nоб: {self.changing_params["arp"]}/{self.attributes["armor"]}\
            \nурон огнем: {self.changing_params["fire_dmg"]}\nурон морозом: {self.changing_params["frost_dmg"]}\nурон электричеством: {self.changing_params["shock_dmg"]}\
            \nурон ядом: {self.changing_params["poison_dmg"]}\nкровотечение: {self.changing_params["bleeding"]}"
            
    def compare_attributes(self,attr1,attr2):
        total=attr1+attr2
        number=random.randrange(total)
        return number<attr1
    
class BerserkSwordsman(Swordsman):
    def __init__(self,name):
        super().__init__(name,SwordsmenClasses.BERSERK.value)
        
def create_swordsman(name,class_name):
    match class_name:
        case SwordsmenClasses.BERSERK.value:
            return BerserkSwordsman(name)
        case _:
            raise TypeError(f"Класс {class_name} не существует")
        
def get_classes_list():
    return [i.value for i in SwordsmenClasses]