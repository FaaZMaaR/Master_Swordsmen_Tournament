import random
import swordsmen

class Duel:
    def __init__(self,pair,swordsmen):
        self.pair=pair
        self.cast_lots(swordsmen)
        self.attacker.reset_changing_params()
        self.defender.reset_changing_params()
        self.summary=dict()
        for v in self.pair["pair"]:
            self.summary[v]={"damage":0,"blocks":0,"healed hp":0}
    
    def cast_lots(self,swordsmen):
        if self.compare_attributes(swordsmen[0].attributes["initiative"],swordsmen[1].attributes["initiative"]):
            self.attacker=swordsmen[0]
            self.defender=swordsmen[1]
        else:
            self.attacker=swordsmen[1]
            self.defender=swordsmen[0]
    
    def pass_move(self):
        tmp=self.attacker
        self.attacker=self.defender
        self.defender=tmp
        self.attacker.recover()
        if self.attacker.changing_params["hp"]<=0:
            self.pair["winner"]=self.defender.name
            return f"Поединок окончен. Победитель - {self.pair["winner"]}."
        else:
            return f"Ход {self.attacker.name}.\n{self.attacker.get_current_params()}"
            
    def first_move(self):
        return f"Ход {self.attacker.name}.\n{self.attacker.get_current_params()}"
        
    def make_attacker_move(self,action):
        self.attacker.action=action
        match action:
            case swordsmen.Actions.ATTACK:
                return f"{self.attacker.name} атакует..."
            case swordsmen.Actions.SPECIAL:
                return f"{self.attacker.name} совершает особую атаку..."
            case swordsmen.Actions.HEAL:
                return f"{self.attacker.name} лечится..."
            case _:
                return f"{self.attacker.name} завершает ход..."
        
    
    def make_defender_move(self,action):
        self.defender.action=action
        match action:
            case swordsmen.Actions.BLOCK:
                return f"\n...{self.defender.name} пытается заблокировать атаку"
            case swordsmen.Actions.DODGE:
                return f"\n...{self.defender.name} пытается увернуться от особой атаки"
            case swordsmen.Actions.COUNTER:
                return f"\n...{self.defender.name} пытается парировать атаку"
            case _:
                return f"\n...{self.defender.name} ждет"
    
    def execute_all_actions(self):
        if self.attacker.action==swordsmen.Actions.ATTACK:
            block=0
            if self.defender.action==swordsmen.Actions.BLOCK:
                block=self.defender.block()                
            attack_result=self.attacker.attack(block,self.defender)
            if attack_result[0]==self.defender.name:
                self.summary[self.defender.name]["blocks"]+=1
            else:
                self.summary[self.attacker.name]["damage"]+=attack_result[1]+attack_result[2]
            if attack_result[1]==0 and attack_result[2]==0:
                return f"{self.defender.name} заблокировал атаку."
            else:
                return f"{self.attacker.name} нанес {attack_result[2]} урона броне и {attack_result[1]} урона здоровью {self.defender.name}"
        elif self.attacker.action==swordsmen.Actions.HEAL:
            heal_result=self.attacker.heal()
            self.summary[self.attacker.name]["healed hp"]+=heal_result[0]
            return f"{self.attacker.name} вылечил {heal_result[0]} очков здоровья и снизил кровотечение на {heal_result[1]} очков"
        else:
            return f"{self.attacker.name} завершил ход."
    
    def show_summary(self):
        s=f"Победитель - {self.pair["winner"]}!\n\nБоевая сводка:\n\n"
        for v in self.summary:
            s+=f"{v}:\nНанес урона - {self.summary[v]["damage"]}\nЗаблокировал атак - {self.summary[v]["blocks"]}\nВылечил здоровья - {self.summary[v]["healed hp"]}\n\n"
        return s
    
    def compare_attributes(self,attr1,attr2):
        total=attr1+attr2
        number=random.randrange(total)
        return number<attr1