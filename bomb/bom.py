from tkinter import*
import time
import random

class Spel:
    def __init__(self):
        self.tk=Tk()
        self.tk.title("bomspel")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas=Canvas(self.tk, width=500, height=500, highlightthickness=0, bd=0)
        self.canvas.pack()
        self.tk.update()
        self.index=0
        self.stc=0
        self.astc=0
        self.tstc=0
        self.health=5
        self.ufos_hit=0
        self.ufos_need=0
        self.stage=0
        self.bosshealth=0
        self.bossufo_width=0
        self.bossufo_height=0
        self.bomb_width=0
        self.bomb_height=0
        self.time=time.time()
        self.size=1
        self.stat1=self.canvas.create_text(45, 7, text="ufo's killed: %s/%s" %(self.ufos_hit, self.ufos_need), state="hidden")
        self.stat2=self.canvas.create_text(25, 20, text="health: %s" %(self.health), state="hidden")
        self.stat3=self.canvas.create_text(480, 7, text="stage %s" %(self.stage), state="hidden")
        self.wintext=self.canvas.create_text(240, 220, text="YOU WIN!", fill="green", font=("times", 1), state="hidden")
        self.losetext=self.canvas.create_text(235, 220, text="defeated", fill="red", font=("times", 1), state="hidden")
        self.weapons=[]
        self.buttons=[]
        self.ufos=[]
        self.uforulers=[]
        self.ufoboss=[]
        self.boollose=False
        self.boolwin=False
        self.start=False
        self.boss=False

    def win(self):
        self.canvas.itemconfig(self.wintext, state="normal")
        self.canvas.itemconfig(self.stat1, text="bosshealth: %s" %self.bosshealth)
        self.health=5
        self.ufos_hit=0
        self.index=0
        if time.time()-self.time>=0.02:
            self.size+=1
            self.canvas.itemconfig(self.wintext, font=("times", self.size))
            self.time=time.time()
        elif self.size>=40:
            self.canvas.itemconfig(self.wintext, state="hidden")
            self.boolwin=False
            self.size=1
            obj1=self.weapons[0].coords()
            x=200-obj1.x1
            self.canvas.move(self.weapons[0], x, 0)
            self.weapons[0].x=0
            for weapon in self.weapons:
                if weapon==self.weapons[0]:
                    continue
                obj2=weapon.coords()
                x=240-obj2.x1
                self.canvas.move(weapon, x, 0)
                weapon.x=0
            time.sleep(1.5)

    def lose(self):
        self.canvas.itemconfig(self.losetext, state="normal")
        self.health=5
        self.ufos_hit=0
        self.index=0
        if time.time()-self.time>=0.02:
            self.size+=1
            self.canvas.itemconfig(self.losetext, font=("times", self.size))
            self.time=time.time()
        elif self.size>=50:
            self.canvas.itemconfig(self.losetext, state="hidden")
            for ufo in self.ufos:
                ufo.disappear()
            self.boollose=False
            self.size=1
            obj1=self.weapons[0].coords()
            x=200-obj1.x1
            self.canvas.move(self.weapons[0], x, 0)
            self.weapons[0].x=0
            for weapon in self.weapons:
                if weapon==self.weapons[0]:
                    continue
                obj2=weapon.coords()
                x=240-obj2.x1
                self.canvas.move(weapon, x, 0)
                weapon.x=0
            time.sleep(1.5)

    def hoofdlus(self):
        while 1:
            if self.start:
                self.canvas.itemconfig(self.stat1, text="ufo's killed: %s/%s" %(self.ufos_hit, self.ufos_need), state="normal")
                self.canvas.itemconfig(self.stat2, text="health: %s" %(self.health), state="normal")
                self.canvas.itemconfig(self.stat3, text="stage %s" %(self.stage), state="normal")
                for weapon in self.weapons:
                    weapon.act()
                for button in self.buttons:
                    button.disappear()
                for uforuler in self.uforulers:
                    uforuler.rule()
                for ufo in self.ufos:
                    ufo.bombdrop()
                for ufoboss in self.ufoboss:
                    ufoboss.nonactive()
                if self.ufos_hit>=self.ufos_need:
                    self.start=False
                    self.boss=True
                    for ufo in self.ufos:
                        ufo.disappear()
            elif self.boss:
                self.canvas.itemconfig(self.stat1, text="bosshealth: %s" %self.bosshealth)
                self.canvas.itemconfig(self.stat2, text="health: %s" %(self.health))
                for bossufo in self.ufoboss:
                    bossufo.act()
                for weapon in self.weapons:
                    weapon.act()
                if self.bosshealth<=0:
                    self.boolwin=True
                    self.boss=False
                    for bossufo in self.ufoboss:
                        bossufo.disappear()
            elif self.boollose:
                self.lose()
            elif self.boolwin:
                self.win()
            else:
                for weapon in self.weapons:
                    weapon.menu()
                for button in self.buttons:
                    button.menu()
                for ufo in self.ufos:
                    ufo.menu()
                for boss in self.ufoboss:
                    boss.disappear()
                self.canvas.itemconfig(self.stat1, state="hidden")
                self.canvas.itemconfig(self.stat2, state="hidden")
                self.canvas.itemconfig(self.stat3, state="hidden")
                self.ufos_hit=0
                self.index=0
            if self.health<=0:
                self.boollose=True
                self.start=False
                self.boss=False
                self.canvas.itemconfig(self.stat2, text="health: %s" %self.health)
                self.health=5
                self.ufos_hit=0
                self.index=0
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

def collision_rocket_ufo(obj1, obj2):
    if obj1.y1<=obj2.y2:
        if obj1.x1<=obj2.x2 and obj1.x2>=obj2.x1:
            return True
        return False

def collision_bomb_weapon(obj1, obj2):
    if obj1.y2>=obj2.y1:
        if obj1.x1<=obj2.x2 and obj1.x2>=obj2.x1:
            return True
        return False
    
class Weapon:
    def __init__(self, g):
        self.g=g
        self.coordinates=None
        
    def act(self):
        pass

    def endact(self):
        pass
    
    def coords(self):
        return self.coordinates


class Raket(Weapon):
    def __init__(self, g, photo):
        Weapon.__init__(self, g)
        self.photo=photo
        self.id=g.canvas.create_image(240, 400, image=self.photo, anchor="nw", state="hidden")
        self.coordinates=Coords()
        self.y=0
        self.x=0
        self.hit_ufo=False
        
    def sfire(self):
        self.x=0
        self.y=-8
        self.g.canvas.itemconfig(self.id, state="normal")

    def coords(self):
        xy=list(self.g.canvas.coords(self.id))
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+15
        self.coordinates.y2=xy[1]+62
        return self.coordinates

    def act(self):
        co=self.coords()
        rco=g.weapons[0].coords()
        if co.y1<=0 or self.hit_ufo:
            self.x=((rco.x1+rco.x2)/2)-co.x1
            self.y=((rco.y1+rco.y2)/2)-co.y1
            self.g.canvas.itemconfig(self.id, state="hidden")
            self.g.canvas.move(self.id, self.x-5, self.y)
            self.x=g.weapons[0].x
            self.y=0
            self.hit_ufo=False
        self.g.canvas.move(self.id, self.x, self.y)

    def menu(self):
        self.g.canvas.itemconfig(self.id, state="hidden")
        

class Raketwerper(Weapon):
    def __init__(self, g, photo):
        Weapon.__init__(self, g)
        self.photo=photo
        self.id=g.canvas.create_image(200, 400, image=self.photo, anchor="nw", state="hidden")
        self.x=0
        self.coordinates=Coords()
        g.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        g.canvas.bind_all("<KeyPress-Right>", self.turn_right)
        g.canvas.bind_all("<KeyPress-Down>", self.stop)
        g.canvas.bind_all("<space>", self.fire)

    def turn_left(self, evt):
        if g.start or g.boss:
            self.x=-4
            for weapon in g.weapons:
                if weapon==self:
                    continue
                if weapon.y==0:
                    weapon.x=-4

    def turn_right(self, evt):
        if g.start or g.boss:
            self.x=4
            for weapon in g.weapons:
                if weapon==self:
                    continue
                if weapon.y==0:
                    weapon.x=4
           
    def stop(self, evt):
        self.x=0
        for weapon in g.weapons:
                if weapon==self:
                    continue
                if weapon.y==0:
                    weapon.x=0

    def fire(self, evt):
        for weapon in g.weapons:
            if weapon==self:
                continue
            if weapon.y!=0:
                continue
            if weapon.y==0:
                weapon.sfire()
                break

    def coords(self):
        xy=list(self.g.canvas.coords(self.id))
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+75
        self.coordinates.y2=xy[1]+100
        return self.coordinates

    def act(self):
        self.g.canvas.itemconfig(self.id, state="normal")
        co=self.coords()
        if co.x1<=0 and self.x<0 or co.x2>=500 and self.x>0:
            self.x=0
            for weapon in g.weapons:
                if weapon==self:
                    continue
                weapon.x=0
        self.g.canvas.move(self.id, self.x, 0)

    def menu(self):
        self.g.canvas.itemconfig(self.id, state="hidden")


class Uforuler:
    def __init__(self, g):
        self.g=g
        self.imglist=[PhotoImage(file="images\\bom.gif"), PhotoImage(file="images\\bom2.gif"),
                      PhotoImage(file="images\\bom3.gif"), PhotoImage(file="images\\bom4.gif"),
                      PhotoImage(file="images\\bom5.gif"), PhotoImage(file="images\\ufo.gif")]
        self.stcc=time.time()
        self.spawntime=time.time()
        self.coordinates=Coords()
        self.coordinates2=Coords()
        self.y=2
        self.ycvr=0
        self.exist=True
        self.bombexist=True
        self.bombindex=0
        self.bombtime=time.time()
        self.time=time.time()

    def stccc(self):
        if time.time()-self.stcc>g.tstc:
            self.stcc=time.time()
            if g.stc>1:
                g.stc-=g.astc
    
    def rule(self):
        self.stccc()
        if time.time()-self.spawntime>g.stc:
            self.spawntime=time.time()
            ufo=Ufo(g)
            g.ufos.append(ufo)
            g.ufos[g.index].spawn()

    def menu(self):
        self.spawntime=time.time()
        self.stcc=time.time()
        for x in range(len(g.ufos)):
            del(g.ufos[0])
        

class Ufo(Uforuler):
    def __init__(self, g):
        Uforuler.__init__(self, g)
        self.id=g.canvas.create_image(500, 20, image=self.imglist[5], anchor="nw")
        self.id2=g.canvas.create_image(500, 0, image=self.imglist[0], anchor="nw")

    def coords(self):
        xy=list(self.g.canvas.coords(self.id))
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+60
        self.coordinates.y2=xy[1]+40
        return self.coordinates

    def coords2(self):
        xy=list(self.g.canvas.coords(self.id2))
        self.coordinates2.x1=xy[0]
        self.coordinates2.y1=xy[1]
        self.coordinates2.x2=xy[0]+44
        self.coordinates2.y2=xy[1]+62
        return self.coordinates2

    def spawn(self):
        rndint=random.randrange(-500, -60)
        self.g.canvas.move(g.ufos[g.index].id, rndint, 0)
        self.g.canvas.move(g.ufos[g.index].id2, rndint, 0)
        g.index+=1

    def bombanimation(self):
        if time.time()-self.bombtime>0.8 and self.bombindex<4:
            self.bombindex+=1
            self.g.canvas.itemconfig(self.id2, image=self.imglist[self.bombindex])
            self.bombtime=time.time()
            if self.bombexist==False:
                self.bombindex=0
            

    def bombdrop(self):
        if self.exist:
            self.bombanimation()
            if self.bombexist:
                self.g.canvas.itemconfig(self.id2, state="normal")
            if time.time()-self.time>=2:
                self.y=2
                self.bombexist=True
            obj1=self.coords() # ufo
            obj2=self.coords2() # bom
            obj3=g.weapons[0].coords() # raketwerper
            for weapon in g.weapons:
                if weapon==g.weapons[0]:
                    continue
                obj4=weapon.coords() # raket
                if collision_rocket_ufo(obj4, obj1):
                    self.g.canvas.itemconfig(self.id, state="hidden")
                    self.g.canvas.itemconfig(self.id2, state="hidden")
                    weapon.hit_ufo=True
                    g.ufos_hit+=1
                    self.exist=False
                if collision_bomb_weapon(obj2, obj4):
                    self.explode()
                    weapon.hit_ufo=True
                    self.bombexist=False
            if obj2.y2>=500:
                    self.g.canvas.move(self.id2, 0, -self.ycvr)
                    self.ycvr=0
                    self.bombindex=0
                    self.g.canvas.itemconfig(self.id2, image=self.imglist[self.bombindex])
            if collision_bomb_weapon(obj2, obj3):
                g.health-=1
                self.explode()
                self.bombexist=False
            self.g.canvas.move(self.id2, 0, self.y)
            self.ycvr+=self.y

    def explode(self):
        self.g.canvas.itemconfig(self.id2, state="hidden")
        self.g.canvas.move(self.id2, 0, -self.ycvr)
        self.ycvr=0
        self.y=0
        self.time=time.time()

    def disappear(self):
      self.g.canvas.itemconfig(self.id, state="hidden")
      self.g.canvas.itemconfig(self.id2, state="hidden")

class Bossufo:
    def __init__(self, g):
        self.g=g
        self.imglist=[PhotoImage(file="images\\ufost1.gif"), PhotoImage(file="images\\ufost2.gif"),
                      PhotoImage(file="images\\ufost3.gif"), PhotoImage(file="images\\ufost4.gif"),
                      PhotoImage(file="images\\bombst1.gif"), PhotoImage(file="images\\bomst2.gif")]
        self.id=g.canvas.create_image(250, 20, image=self.imglist[0], anchor="nw", state="hidden")
        self.photo=PhotoImage(file="images\\bom.gif")
        self.bomb1=g.canvas.create_image(270, 20, image=self.photo, anchor="nw", state="hidden")
        self.bomb2=g.canvas.create_image(270, 20, image=self.photo, anchor="nw", state="hidden")
        self.bomb3=g.canvas.create_image(270, 20, image=self.photo, anchor="nw", state="hidden")
        self.bomb4=g.canvas.create_image(270, 20, image=self.photo, anchor="nw", state="hidden")
        self.bomb5=g.canvas.create_image(270, 20, image=self.photo, anchor="nw", state="hidden")
        self.bomblist=[self.bomb1, self.bomb2, self.bomb3, self.bomb4, self.bomb5]
        self.boolbomb={self.bomb1:True, self.bomb2:True, self.bomb3:True, self.bomb4:True, self.bomb5:True} 
        self.x=-2
        self.bombx=0
        self.y=0
        self.bombindex=0
        self.bombindex2=0
        self.steps=0
        self.stopped=False
        self.randomdone=False
        self.movetime=time.time()
        self.bombtime=time.time()
        self.coordinates=Coords()
        self.bombcoordinates=Coords()

    def coords(self):
        xy=list(self.g.canvas.coords(self.id))
        self.coordinates.x1=xy[0]
        self.coordinates.y1=xy[1]
        self.coordinates.x2=xy[0]+g.bossufo_width
        self.coordinates.y2=xy[1]+g.bossufo_height
        return self.coordinates

    def bombcoords(self):
        xy=list(self.g.canvas.coords(self.bomblist[self.bombindex2]))
        self.bombcoordinates.x1=xy[0]
        self.bombcoordinates.y1=xy[1]
        self.bombcoordinates.x2=xy[0]+g.bomb_width
        self.bombcoordinates.y2=xy[1]+g.bomb_height
        return self.bombcoordinates

    def nonactive(self):
        self.movetime=time.time()
        self.bombtime=time.time()

    def act(self):
        self.g.canvas.itemconfig(self.id, state="normal", image=self.imglist[g.stage-1])
        for bomb in self.bomblist:
            if g.stage>=3:
                photo=self.imglist[5]
            else:
                photo=self.imglist[4]
            self.g.canvas.itemconfig(bomb, image=photo)
        obj1=self.coords()
        obj2=g.weapons[0].coords()
        for weapon in g.weapons:
            if weapon==g.weapons[0]:
                continue
            obj3=weapon.coords() # raket
            if collision_rocket_ufo(obj3, obj1):
                weapon.hit_ufo=True
                g.bosshealth-=1
            for i in range(len(self.bomblist)):
                if self.stopped:
                    self.bombindex2=i
                    obj4=self.bombcoords()
                    if collision_bomb_weapon(obj4, obj3):
                        weapon.hit_ufo=True
                        y=((obj1.y1+obj1.y2)/2)-obj4.y1
                        self.g.canvas.move(self.bomblist[i], 0,  y)
                        self.boolbomb[i+19]=False
                        self.g.canvas.itemconfig(self.bomblist[i], state="hidden")
        for i in range(len(self.bomblist)):
            self.bombindex2=i
            obj4=self.bombcoords()
            if collision_bomb_weapon(obj4, obj2):
                g.health-=1
                y=((obj1.y1+obj1.y2)/2)-obj4.y1
                self.g.canvas.move(self.bomblist[i], 0,  y)
                self.boolbomb[i+19]=False
                self.g.canvas.itemconfig(self.bomblist[i], state="hidden")
        for i in range(len(self.bomblist)):
            self.bombindex2=i
            obj3=self.bombcoords()
            if obj3.y2>=500:
                y=((obj1.y1+obj1.y2)/2)-obj3.y1
                self.g.canvas.move(self.bomblist[i], 0, y)
                self.boolbomb[i+19]=False
                self.g.canvas.itemconfig(self.bomblist[i], state="hidden")
        if time.time()-self.bombtime>=0.1 and self.stopped:
            self.bombtime=time.time()
            self.bombindex+=1
        if not self.randomdone:
            global rndm
            rndm=random.randrange(150, 250)
            self.randomdone=True
        if abs(self.steps)>=rndm or obj1.x1<0 or obj1.x2>500:
            if self.x!=0:
                self.wasx=self.x
            self.x=0
            self.stopped=True
            self.y=g.stage+3
        if not self.stopped:
            self.steps+=self.x*g.stage
        for x in range(len(self.bomblist)):
            if not self.stopped:
                self.g.canvas.move(self.bomblist[x], self.x*g.stage, 0)
        self.g.canvas.move(self.id, self.x*g.stage, 0)
        if self.stopped:
            if g.stage>=3:
                if self.bombx==0:
                    self.bombx=0
            for y in range(0, 5):
                if y>self.bombindex:
                    break
                elif self.boolbomb[y+19]==True:
                    self.bombindex2=y
                    obj3=self.bombcoords()
                    self.g.canvas.itemconfig(self.bomblist[y], state="normal")
                    self.g.canvas.move(self.bomblist[y], self.bombx, self.y)
        for i in range(len(self.boolbomb)+1):
            if i!=5:
                if self.boolbomb[i+19]==True:
                    break
            elif i==5:
                self.stopped=False
                self.steps=0
                self.randomdone=False
                self.x=-self.wasx
                self.g.canvas.move(self.id, self.x*g.stage, 0)
                self.bombindex=0
                for x in range(len(self.boolbomb)):
                    self.boolbomb[x+19]=True

    def disappear(self):
        self.g.canvas.itemconfig(self.id, state="hidden")
        for bomb in self.bomblist:
            self.g.canvas.itemconfig(bomb, state="hidden")
        
        

class Buttons:
    def __init__(self, x1, y1, x2, y2, g, text, fill):
        self.g=g
        self.text=text
        self.fill=fill
        self.id=g.canvas.create_rectangle(x1, y1, x2, y2, fill=self.fill)
        self.id2=g.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=self.text)
        g.canvas.bind_all("<Button-1>", self.start)

    def start(self, event):
        if not g.start:
            if event.x>=150 and event.x<=350:
                if event.y>=75 and event.y<=125:
                    g.start=True
                    g.stc=3
                    g.astc=0.2
                    g.tstc=10
                    g.ufos_need=25
                    g.stage=1
                    g.bossufo_width=130
                    g.bossufo_height=80
                    g.bomb_width=60
                    g.bomb_height=85
                    g.bosshealth=20
                if event.y>=175 and event.y<=225:
                    g.start=True
                    g.stc=3
                    g.astc=0.2
                    g.tstc=7.5
                    g.ufos_need=35
                    g.stage=2
                    g.bossufo_width=160
                    g.bossufo_height=80
                    g.bomb_width=60
                    g.bomb_height=85
                    g.bosshealth=30
                if event.y>=275 and event.y<=325:
                    g.start=True
                    g.stc=3
                    g.astc=0.2
                    g.tstc=5
                    g.ufos_need=50
                    g.stage=3
                    g.bossufo_width=190
                    g.bossufo_height=100
                    g.bomb_width=80
                    g.bomb_height=110
                    g.bosshealth=40
                if event.y>=375 and event.y<=425:
                    g.start=True
                    g.stc=3
                    g.astc=0.2
                    g.tstc=2.5
                    g.ufos_need=65
                    g.stage=4
                    g.bossufo_width=220
                    g.bossufo_height=125
                    g.bomb_width=80
                    g.bomb_height=110
                    g.bosshealth=50

    def disappear(self):
        self.g.canvas.itemconfig(self.id, state="hidden")
        self.g.canvas.itemconfig(self.id2, state="hidden")

    def menu(self):
        self.g.canvas.itemconfig(self.id, state="normal")
        self.g.canvas.itemconfig(self.id2, state="normal")
        
        

g=Spel()
button1=Buttons(150, 75, 350, 125, g, "stage 1", "green")
button2=Buttons(150, 175, 350, 225, g, "stage 2", "blue")
button3=Buttons(150, 275, 350, 325, g, "stage 3", "yellow")
button4=Buttons(150, 375, 350, 425, g, "stage 4", "red")
g.buttons.append(button1)
g.buttons.append(button2)
g.buttons.append(button3)
g.buttons.append(button4)
raketwerper=Raketwerper(g, PhotoImage(file="images\\raketwerper.gif"))
raket1=Raket(g, PhotoImage(file="images\\rocket.gif"))
raket2=Raket(g, PhotoImage(file="images\\rocket.gif"))
raket3=Raket(g, PhotoImage(file="images\\rocket.gif"))
g.weapons.append(raketwerper)
g.weapons.append(raket1)
g.weapons.append(raket2)
g.weapons.append(raket3)
uforuler=Uforuler(g)
bossufo=Bossufo(g)
g.ufoboss.append(bossufo)
g.uforulers.append(uforuler)
g.hoofdlus()
