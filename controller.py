import swordsmen
    
class Controller:
    def __init__(self,attacker,defender):
        self.attacker=attacker
        self.defender=defender
        
    def make_move(self):
        atk_action=swordsmen.Actions.PASS
        dfc_action=swordsmen.Actions.PASS
        if self.attacker.changing_params["ap"]>self.attacker.attributes["initiative"]//2:
            atk_action=swordsmen.Actions.ATTACK
        elif (self.attacker.changing_params["bleeding"]>0 or self.attacker.changing_params["hp"]<self.attacker.attributes["health"]//2) and self.attacker.changing_params["sp"]>=4:
            atk_action=swordsmen.Actions.HEAL
        if atk_action==swordsmen.Actions.ATTACK and self.defender.changing_params["ap"]>=1:
            dfc_action=swordsmen.Actions.BLOCK
        return (atk_action,dfc_action)