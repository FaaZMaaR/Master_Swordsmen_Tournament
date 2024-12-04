import itertools
import random
from PIL import Image,ImageDraw,ImageFont

class NotEnoughContestantsError(Exception):
    pass
class ContestantCountError(Exception):
    pass
class TooManyContestantsError(Exception):
    pass
class NoFreePairsError(Exception):
    pass
class UndueledPairsRemainError(Exception):
    pass

class Tournament:
    def __init__(self,contestant_count):
        if contestant_count not in (2,4,8,16): raise ContestantCountError
        self.contestant_count=contestant_count
        self.contestants_dict=dict()
        self.stages_dict=dict()
        self.stages_list=["first","second","third","forth"]
        self.stage=0
        
    def add_contestant(self,contestant):
        if len(self.contestants_dict)==self.contestant_count: raise TooManyContestantsError
        self.contestants_dict[contestant.name]=contestant
        
    def assign_contestants(self):
        if len(self.contestants_dict)!=self.contestant_count: raise NotEnoughContestantsError
        combs=list(itertools.combinations(self.contestants_dict,2))
        self.stages_dict["first"]=list()
        for i in range(len(self.contestants_dict)//2):
            picked=False
            while not picked:
                picked=True
                chosen=random.choice(combs)
                for v in self.stages_dict["first"]:
                    if chosen[0] in v["pair"] or chosen[1] in v["pair"]:
                        combs.remove(chosen)
                        picked=False
                        break   
            self.stages_dict["first"].append({"pair":chosen,"winner":""})
            
    def get_table_image(self):
        rectw=150
        recth=20     
        img = Image.new('RGBA', (10+len(self.stages_dict)*200, 10+len(self.stages_dict["first"])*2*40), 'white')    
        idraw = ImageDraw.Draw(img)
        font=ImageFont.truetype("arial.ttf",size=14)
        i=0        
        for k in self.stages_dict:
            x0=10+200*i
            y0=10+(2**i-1)*2*recth
            for j in range(len(self.stages_dict[k])):
                x1=x0
                y1=y0+(2**i)*4*recth*j
                idraw.rectangle((x1,y1,x1+rectw,y1+recth), outline='blue',width=2)
                idraw.text((x1+5,y1+2),self.stages_dict[k][j]["pair"][0],fill="black",font=font)
                idraw.rectangle((x1,y1+recth,x1+rectw,y1+2*recth), outline='blue',width=2)
                idraw.text((x1+5,y1+recth+2),self.stages_dict[k][j]["pair"][1],fill="black",font=font)
                if i!=0:
                    idraw.line((x2+rectw,y2+(2**(i-1))*8*recth*j+recth,x1+rectw//2,y2+(2**(i-1))*8*recth*j+recth),fill="blue",width=2)
                    idraw.line((x2+rectw,y2+(2**(i-1))*8*recth*j+(2**(i-1))*4*recth+recth,x1+rectw//2,y2+(2**(i-1))*8*recth*j+(2**(i-1))*4*recth+recth),fill="blue",width=2)
                    idraw.line((x1+rectw//2,y2+(2**(i-1))*8*recth*j+recth,x1+rectw//2,y1),fill="blue",width=2)
                    idraw.line((x1+rectw//2,y2+(2**(i-1))*8*recth*j+(2**(i-1))*4*recth+recth,x1+rectw//2,y1+2*recth),fill="blue",width=2)
            i+=1
            x2=x0
            y2=y0
        return img
    
    def assign_duelists(self):
        for v in self.stages_dict[self.stages_list[self.stage]]:
            if v["winner"]=="":
                return v
        raise NoFreePairsError
    
    def move_to_next_stage(self):
        i=0
        for v in self.stages_dict[self.stages_list[self.stage]]:
            if v["winner"]=="": return (0,len(self.stages_dict[self.stages_list[self.stage]])-i)
            i+=1
        if len(self.stages_dict[self.stages_list[self.stage]])==1:
            return (2,self.stages_dict[self.stages_list[self.stage]][0]["winner"])
        else:
            self.stages_dict[self.stages_list[self.stage+1]]=[]
            for i in range(len(self.stages_dict[self.stages_list[self.stage]])//2):
                self.stages_dict[self.stages_list[self.stage+1]].append({"pair":(self.stages_dict[self.stages_list[self.stage]][i*2]["winner"],self.stages_dict[self.stages_list[self.stage]][i*2+1]["winner"]),"winner":""})
            self.stage+=1
            return (1,self.stage)