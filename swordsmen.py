import random
import enum

class SwordsmenClasses(enum.Enum):    
    DEFAULT=""
    BERSERK="Мечник Берсерк"
    FIRE="Мечник Огня"
    FROST="Мечник Мороза"
    SHOCK="Мечник Молнии"
    ASSASSIN="Мечник Убийца"
    #PALADIN="Мечник Паладин"
    #SORCERER="Мечник Колдун"
    
class Actions(enum.Enum):
    PASS=enum.auto()
    ATTACK=enum.auto()
    SPECIAL=enum.auto()
    HEAL=enum.auto()
    BLOCK=enum.auto()
    DODGE=enum.auto()
    COUNTER=enum.auto()

class Swordsman:
    def __init__(self,name,class_name=SwordsmenClasses.DEFAULT.value,attributes=None,skills=None,resistance=None,recovering=None,costs=None):
        self.name=name
        self.class_name=class_name
        
        self.attributes={"health":100,"initiative":15,"skill":12,"armor":100} if attributes==None else attributes
        self.skills={"attacking":50,"defence":50,"dodging":25,"mastery":25,"healing":25} if skills==None else skills
        self.resistance={"heat":15,"cold":15,"shock":15,"poison":15,"curse":15} if resistance==None else resistance
        self.recovering={"ap":10,"sp":4} if recovering==None else recovering
        self.costs={"attack":4,"block":2,"dodge":3,"heal":4,"special":6} if costs==None else costs
        
        self.reset_changing_params()
        
        self.action=Actions.PASS
    
    def attack(self,block,defender):
        self.changing_params["ap"]-=self.costs["attack"]
        attack=self.skills["attacking"]
        hp_dmg=0
        arp_dmg=0
        if block>0:
            if self.compare_attributes(attack,block):
                attack=random.randrange(attack//2,attack+1)
            else:
                return (defender.name,hp_dmg,arp_dmg)
        if defender.changing_params["arp"]<attack:
            hp_dmg=attack-defender.changing_params["arp"]
            attack-=hp_dmg
        arp_dmg=random.randrange(attack+1)
        defender.changing_params["hp"]-=hp_dmg
        defender.changing_params["arp"]-=arp_dmg
        return (self.name,hp_dmg,arp_dmg)
    
    def block(self):
        self.changing_params["ap"]-=self.costs["block"]
        return self.skills["defence"]
    
    def dodge(self):
        self.changing_params["ap"]-=self.costs["dodge"]
        return self.skills["dodging"]
    
    def counter(self,attacker):
        self.changing_params["ap"]-=(self.costs["attack"]-self.costs["block"])
        attack=self.skills["attacking"]//2
        hp_dmg=0
        arp_dmg=0
        if attacker.changing_params["arp"]<attack:
            hp_dmg=attack-attacker.changing_params["arp"]
            attack-=hp_dmg
        arp_dmg=random.randrange(attack+1)
        attacker.changing_params["hp"]-=hp_dmg
        attacker.changing_params["arp"]-=arp_dmg
        return (self.name,hp_dmg,arp_dmg)
    
    def do_special(self,spec,dodge,defender):
        self.changing_params["sp"]-=self.costs["special"]
        special=self.skills["mastery"]
        hp_dmg=0
        spec_dmg=0
        if dodge>0:
            if self.compare_attributes(special,dodge):
                special=random.randrange(special//2,special+1)
            else:
                return (defender.name,hp_dmg,spec_dmg)
        if defender.changing_params["arp"]<special:
            hp_dmg=special-defender.changing_params["arp"]
            special-=hp_dmg
        init_special=special-defender.changing_params["arp"]
        if init_special<0: init_special=0
        spec_dmg=random.randrange(init_special,special+1)//2
        defender.changing_params["hp"]-=hp_dmg
        defender.changing_params[spec]+=spec_dmg
        return (self.name,hp_dmg,spec_dmg,spec)
    
    def do_no_dodging_special(self):
        pass    
    
    def heal(self):        
        self.changing_params["sp"]-=self.costs["heal"]
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
        super().__init__(name,SwordsmenClasses.BERSERK.value,
                         attributes={"health":125,"initiative":16,"skill":10,"armor":110},
                         skills={"attacking":90,"defence":60,"dodging":20,"mastery":20,"healing":25},
                         resistance={"heat":20,"cold":20,"shock":20,"poison":20,"curse":15},
                         recovering={"ap":10,"sp":4},
                         costs={"attack":4,"block":2,"dodge":3,"heal":4,"special":6})
        self.special_damage="bleeding"
    
    def do_special(self,dodge,defender):
        return super().do_special(self.special_damage,dodge,defender)

class FireSwordsman(Swordsman):
    def __init__(self,name):
        super().__init__(name,SwordsmenClasses.FIRE.value,
                         attributes={"health":100,"initiative":15,"skill":15,"armor":100},
                         skills={"attacking":60,"defence":50,"dodging":25,"mastery":40,"healing":20},
                         resistance={"heat":50,"cold":10,"shock":20,"poison":15,"curse":15},
                         recovering={"ap":10,"sp":6},
                         costs={"attack":4,"block":2,"dodge":3,"heal":4,"special":5})
        self.special_damage="fire_dmg"
        
    def do_special(self,dodge,defender):
        return super().do_special(self.special_damage,dodge,defender)
        
class FrostSwordsman(Swordsman):
    def __init__(self,name):
        super().__init__(name,SwordsmenClasses.FROST.value,
                         attributes={"health":140,"initiative":12,"skill":15,"armor":120},
                         skills={"attacking":40,"defence":80,"dodging":20,"mastery":40,"healing":20},
                         resistance={"heat":20,"cold":50,"shock":10,"poison":15,"curse":15},
                         recovering={"ap":9,"sp":6},
                         costs={"attack":4,"block":2,"dodge":3,"heal":4,"special":5})
        self.special_damage="frost_dmg"
    
    def do_special(self,dodge,defender):
        return super().do_special(self.special_damage,dodge,defender)
        
class ShockSwordsman(Swordsman):
    def __init__(self,name):
        super().__init__(name,SwordsmenClasses.SHOCK.value,
                         attributes={"health":100,"initiative":15,"skill":15,"armor":100},
                         skills={"attacking":50,"defence":50,"dodging":25,"mastery":40,"healing":20},
                         resistance={"heat":10,"cold":20,"shock":50,"poison":15,"curse":15},
                         recovering={"ap":10,"sp":6},
                         costs={"attack":4,"block":2,"dodge":3,"heal":4,"special":5})
        self.special_damage="shock_dmg"
        
    def do_special(self,dodge,defender):
        return super().do_special(self.special_damage,dodge,defender)
        
class AssassinSwordsman(Swordsman):
    def __init__(self,name):
        super().__init__(name,SwordsmenClasses.ASSASSIN.value,
                         attributes={"health":90,"initiative":20,"skill":10,"armor":85},
                         skills={"attacking":40,"defence":40,"dodging":50,"mastery":25,"healing":40},
                         resistance={"heat":15,"cold":15,"shock":15,"poison":50,"curse":15},
                         recovering={"ap":12,"sp":4},
                         costs={"attack":4,"block":2,"dodge":2,"heal":4,"special":6})
        self.special_damage="poison_dmg"
        
    def do_special(self,dodge,defender):
        return super().do_special(self.special_damage,dodge,defender)
        
def create_swordsman(name,class_name):
    match class_name:
        case SwordsmenClasses.BERSERK.value:
            return BerserkSwordsman(name)
        case SwordsmenClasses.FIRE.value:
            return FireSwordsman(name)
        case SwordsmenClasses.FROST.value:
            return FrostSwordsman(name)
        case SwordsmenClasses.SHOCK.value:
            return ShockSwordsman(name)
        case SwordsmenClasses.ASSASSIN.value:
            return AssassinSwordsman(name)
        case _:
            raise TypeError(f"Класс {class_name} не существует")
        
def get_classes_list():
    return [i.value for i in SwordsmenClasses]