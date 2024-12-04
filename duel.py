import random
import swordsmen

class Duel:
    def __init__(self,pair,swordsmen):
        self.pair=pair
        self.cast_lots(swordsmen)
        self.attacker.reset_changing_params()
        self.defender.reset_changing_params()
    
    def cast_lots(self,swordsmen):
        if self.compare_attributes(swordsmen[0].attributes["initiative"],swordsmen[1].attributes["initiative"]):
            swordsmen[0].is_attacking=True
            self.attacker=swordsmen[0]
            swordsmen[1].is_attacking=False
            self.defender=swordsmen[1]
        else:
            swordsmen[1].is_attacking=True
            self.attacker=swordsmen[1]
            swordsmen[0].is_attacking=False
            self.defender=swordsmen[0]
    
    def pass_move(self):
        tmp=self.attacker
        self.attacker=self.defender
        self.defender=tmp
        self.attacker.is_attacking=True
        self.defender.is_attacking=False
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
            attack_result=self.attacker.attack(block,self.defender.changing_params["arp"])
            self.defender.changing_params["hp"]-=attack_result[0]
            self.defender.changing_params["arp"]-=attack_result[1]
            if attack_result[0]==0 and attack_result[1]==0:
                return f"{self.defender.name} заблокировал атаку."
            else:
                return f"{self.attacker.name} нанес {attack_result[1]} урона броне и {attack_result[0]} урона здоровью {self.defender.name}"
        elif self.attacker.action==swordsmen.Actions.HEAL:
            heal_result=self.attacker.heal()
            return f"{self.attacker.name} вылечил {heal_result[0]} очков здоровья и снизил кровотечение на {heal_result[1]} очков"
        else:
            return f"{self.attacker.name} завершил ход."
                    
    
    def compare_attributes(self,attr1,attr2):
        total=attr1+attr2
        number=random.randrange(total)
        return number<attr1