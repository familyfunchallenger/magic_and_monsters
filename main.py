import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import math
import os

TYPE_MONSTER = 0
TYPE_HERO = 1
TYPE_BUILDING = 2

MONSTER_GOOMBA = 0
MONSTER_MINOTAUR = 1
MONSTER_LAISTRYGONIAN = 2
MONSTER_ZOMBIE = 3
MONSTER_DEVIL = 4
MONSTER_SATAN = 5
MONSTER_VAMPIRE = 6
MONSTER_DRAGON = 7
MONSTER_HYDRA = 8
MONSTER_WITHER = 9
MONSTER_NEMEAN_LION = 10

MONSTER_DATA = {
    MONSTER_GOOMBA: {'name': 'Goomba', 'hp': 5, 'lvl': 1},
    MONSTER_MINOTAUR: {'name': 'Minotaur', 'hp': 30, 'lvl': 1},
    MONSTER_LAISTRYGONIAN: {'name': 'Laistrygonian', 'hp': 20, 'lvl': 1},
    MONSTER_ZOMBIE: {'name': 'Zombie', 'hp': 15, 'lvl': 1},
    MONSTER_DEVIL: {'name': 'Devil', 'hp': 25, 'lvl': 1},
    MONSTER_SATAN: {'name': 'Satan', 'hp': 50, 'lvl': 5},
    MONSTER_VAMPIRE: {'name': 'Vampire', 'hp': 15, 'lvl': 1},
    MONSTER_DRAGON: {'name': 'Dragon', 'hp': 50, 'lvl': 5},
    MONSTER_HYDRA: {'name': 'Hydra', 'hp': 60, 'lvl': 7},
    MONSTER_WITHER: {'name': 'Wither', 'hp': 70, 'lvl': 9},
    MONSTER_NEMEAN_LION: {'name': 'Nemean Lion', 'hp': 100, 'lvl': 13},
}

HERO_WARRIOR = 0
HERO_ARCHER = 1
HERO_WIZARD = 2

BUILDING_EMPTY = 0
BUILDING_HOUSE = 1
BUILDING_BAR = 2
BUILDING_PIT = 3
BUILDING_FIRE = 4
BUILDING_TREASURE = 5
BUILDING_KITCHEN = 6

BUILDING_DATA = {
    BUILDING_EMPTY: {
        'name': 'Empty Space', 'hp_impact': 0, 'xp_impact': 0
    },
    BUILDING_HOUSE: {
        'name': 'House', 'hp_impact': 5, 'xp_impact': 0},
    BUILDING_BAR: {
        'name': 'Bar', 'hp_impact': 10, 'xp_impact': 0},
    BUILDING_PIT: {
        'name': 'Pit', 'hp_impact': -20, 'xp_impact': 0},
    BUILDING_FIRE: {
        'name': 'Fire', 'hp_impact': -5, 'xp_impact': 0},
    BUILDING_TREASURE: {
        'name':'Treasure', 'hp_impact': 30, 'xp_impact': 30},
    BUILDING_KITCHEN: {
        'name': 'Kitchen', 'hp_impact': 0, 'xp_impact': 10},
}


class Character(object):
    
   
    def __init__(self,ch_type, subtype, x, y):
        self.type = ch_type
        self.subtype = subtype
        self.name = 'n/a'
        self.level = -1
        self.xp = 0
        self.hp = 0
        self.x = y
        self.y = y

    def __str__(self):
        return '%s/%s' % (self.name[:2], self.hp)

    def LongStr(self):
        return '%s [HP: %s] [Level: %s]' % (self.name, self.hp, self.level)


class Monster(Character):

    def __init__(self, ch_type, subtype, x, y):
        super().__init__(ch_type, subtype, x, y)
        self.ch_type = TYPE_MONSTER
        self.name = MONSTER_DATA[self.subtype]['name']
        self.level = MONSTER_DATA[self.subtype]['lvl']
        self.hp = MONSTER_DATA[self.subtype]['hp']

    


class Hero(Character):

    def __init__(self, ch_type, subtype, x=0, y=0):
        super().__init__(ch_type, subtype,x, y)
        self.type = TYPE_HERO
        self.last_move_direction = -1
        self.name = 'Greg Heffley'
        self.hp = 50
        self.level = 1

    def Reset(self):
        self.last_move_direction = -1
        self.hp = 50
        self.xp = 0
        self.level = 1
        self.x = 0
        self.y = 0

    def MoveOneStepOnMap(self, mapdata):
        # 0 - up, 1 - down, 2 - left, 3 - right
        move_done = False
        while not move_done:
            r = random.randrange(0, 4)
            print('moving direction: ', r)
            if set([r, self.last_move_direction]) == set([0, 1]) or set([r, self.last_move_direction]) == set([3, 2]):
                print('One cannot go back....')
                continue
            if (r == 0 and self.y != 0):
                self.y = self.y - 1
                move_done = True
                self.last_move_direction = r
                continue
            elif (r == 1 and self.y != mapdata.height - 1):
                self.y = self.y + 1
                move_done = True
                self.last_move_direction = r
                continue
            elif (r == 2 and self.x != 0):
                self.x = self.x - 1
                move_done = True
                self.last_move_direction = r
                continue
            elif (r == 3 and self.x != mapdata.width - 1):
                self.x = self.x + 1
                self.last_move_direction = r
                move_done = True
            else:
                continue
        print('Hero position: %s - %s' % (self.x, self.y))

class Building(object):

    def __init__(self, building_type, x, y):
        self.building_type = building_type
        self.x = x
        self.y = y
        self.name = BUILDING_DATA[self.building_type]['name']

    def __str__(self):
        if self.building_type == BUILDING_EMPTY:
            return '    '
        return self.name[0]

    def LongStr(self):
        building_data = BUILDING_DATA[self.building_type]
        return '%s: [HP Impact: %s] [XP Impact: %s]' % (
            building_data['name'], building_data['hp_impact'], building_data['xp_impact']
        )

class Map(object):
    
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.mapdata = [ ['0' for x in range( width )] for y in range( height ) ]

    def InitializeMap(self):
        #random.seed(999)
        for x in range(self.width):
            for y in range(self.height):
                if x == 0 and y == 0:
                    self.mapdata[x][y] = Building(BUILDING_EMPTY, 0, 0)
                    continue
                r = random.randint(0, 1)
                if r == 0:
                    # Create a monster at (x, y)
                    monster_r = random.randint(0, 10)
                    self.mapdata[x][y] = Monster(TYPE_MONSTER, monster_r, x, y)
                elif r == 1:
                    # Create a building at (x, y)
                    building_r = random.randint(0, 48)
                    if (building_r == BUILDING_PIT):
                        building_r = random.randint(0, 6)
                    elif building_r > 6:
                        building_r = 0
                    self.mapdata[x][y] = Building(building_r, x, y)
                else:
                    print('ERROR: something is wrong, aborting....')


    def Print(self):
        for x in range(self.width):
            print()
            for y in range(self.height):
                print('{0:{width}}'.format(str(self.mapdata[x][y]), width=10), end=' ')
        print()


class Application(tk.Frame):

    def CreateWidgets(self):
        self.quit = tk.Button(self, text='QUIT', fg='red',
                              command=self.master.destroy)
        self.quit.pack(side='right')

        self.start = tk.Button(self, text='START', fg='green',
                              command=self.CreateGrid)
        self.start.pack(side='left')

        self.throwDiceToMoveBtn = tk.Button(self, text='Toss Dice and Move', fg='blue', command=self.ThrowDiceAndMove)
        self.throwDiceToMoveBtn.pack(side='bottom')

        #self.throwDiceForFightBtn = tk.Button(self, text='Toss Dice to Fight', fg='red', command=self.ThrowForFight)
        #self.throwDiceForFightBtn.pack(side='bottom')
       
    def ThrowForFight(self):
        r = random.randrange(1, 50)
        print('Hit caused HP loss of ', r)

    def ThrowDiceAndMove(self):
        r = random.randint(1, 12)
        print('You can move %s steps' % r)
        for _ in range(r):
            self.hero.MoveOneStepOnMap(self.mapdata)
            w = self.canvas.winfo_width() # Get current width of canvas
            h = self.canvas.winfo_height() # Get current height of canvas
            cell_width = (int)(w / self.mapdata.width)
            cell_height = (int)(h / self.mapdata.height)
            self.canvas.delete('hero')
            self.canvas.update_idletasks()
            self.canvas.create_image(
                self.hero.x * cell_width + cell_width / 2,
                self.hero.y * cell_height + cell_height / 2, image=self.warrior_img,
                tags='hero')
            self.canvas.update_idletasks()
            self.UpdateLabels()
            time.sleep(1)
        self.root.event_generate('<<HeroDoneMove>>', when='tail')



    def CreateGrid(self, event=None):
        self.mapdata.InitializeMap()
        self.mapdata.Print()
        self.hero.Reset()
        self.throwDiceToMoveBtn['state'] = 'normal'
        
        
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        self.canvas.delete('grid_line') # Will only remove the grid_line
        self.canvas.delete('monsters')
        self.canvas.delete('buildings')
        self.canvas.delete('hero')
        # Creates all vertical lines at intevals of w / mapdata.width
        for i in range(0, w, (int)(w / self.mapdata.width)):
            self.canvas.create_line([(i, 0), (i, h)], width=3, tag='grid_line')

        # Creates all horizontal lines at intevals of h / mapdata.height
        for i in range(0, h, (int)(h / self.mapdata.height)):
            self.canvas.create_line([(0, i), (w, i)], width=3,tag='grid_line')

        self.PopulateGrid()
        if self.first_time_rendering:
            self.LoadLabels()
            self.first_time_rendering = False
        
        
    def LoadLabels(self):
        self.label_text_hero = tk.StringVar()
        self.warrior_img_for_label = self.warrior_img_for_label.resize((50, 50), Image.ANTIALIAS) 
        self.warrior_img_for_label = ImageTk.PhotoImage(self.warrior_img_for_label)
        self.hero_label = tk.Label(
            compound='left',
            image=self.warrior_img_for_label,
            textvariable= self.label_text_hero)
        self.hero_label.pack(side='top')
        
        self.label_text_position = tk.StringVar()
        self.question_mark_img_for_label = self.question_mark_img_for_label.resize((50, 50), Image.ANTIALIAS) 
        self.question_mark_img_for_label = ImageTk.PhotoImage(self.question_mark_img_for_label)
        self.position_label = tk.Label(
            compound='left',
            image=self.building_images[BUILDING_EMPTY]['label'],
            textvariable=self.label_text_position)
        self.position_label.pack(side='top')
        
        self.UpdateLabels()
        
        

    def PopulateGrid(self):
        w = self.canvas.winfo_width() # Get current width of canvas
        h = self.canvas.winfo_height() # Get current height of canvas
        cell_width = (int)(w / self.mapdata.width)
        cell_height = (int)(h / self.mapdata.height)
        self.LoadImages(cell_width, cell_height)
        for x in range(self.mapdata.width):
            for y in range(self.mapdata.height):
                d = self.mapdata.mapdata[x][y]
                #self.canvas.create_text(
                #    x * cell_width + cell_width / 2,
                #    y * cell_height + cell_width / 2,
                #    text=str(d))
                if isinstance(d, Building):
                    self.canvas.create_image(
                        x * cell_width + cell_width / 2,
                        y * cell_height + cell_height / 2,
                        image=self.building_images[d.building_type]['canvas'],
                        tags='buildings') 
                else:
                    self.canvas.create_image(
                      x * cell_width + cell_width / 2,
                      y * cell_height + cell_height / 2,
                      image=self.monster_images[d.subtype]['canvas'],
                      tags='monsters')
        
        self.warrior_img = self.warrior_img_for_canvas.resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS) 
        self.warrior_img = ImageTk.PhotoImage(self.warrior_img)
        self.canvas.create_image(cell_width / 2, cell_height / 2, image=self.warrior_img, tags='hero')
        
    def LoadImages(self, cell_width, cell_height):
        images_dir = os.path.dirname(os.path.realpath(__file__))
        self.warrior_img_for_canvas = Image.open(os.path.join(images_dir, 'warrior.jpg'))
        self.warrior_img_for_label = Image.open(os.path.join(images_dir, 'warrior.jpg'))
        self.question_mark_img_for_label = Image.open(os.path.join(images_dir, 'question-mark.jpg'))
        self.monster_images = {
            MONSTER_GOOMBA: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'GoombaBoii.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'GoombaBoii.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_DEVIL: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'DevilBoi.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'DevilBoi.png')).resize((50, 50), Image.ANTIALIAS)),
            },
             MONSTER_DRAGON: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Dragon_Head.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Dragon_Head.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_HYDRA: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'HydraHeads.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'HydraHeads.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_LAISTRYGONIAN: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Laistrygonian_Giant.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Laistrygonian_Giant.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_MINOTAUR: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'MinotaurBoi.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'MinotaurBoi.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_NEMEAN_LION: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'LionHead.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'LionHead.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_SATAN: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'SatanFace.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'SatanFace.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_VAMPIRE: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'VampireBOI.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'VampireBOI.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_WITHER: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Da_Wither_Boi.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Da_Wither_Boi.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            MONSTER_ZOMBIE: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'ZombiBoi.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'ZombiBoi.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
        }
        self.building_images = {
            BUILDING_BAR: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Bar.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Bar.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            BUILDING_EMPTY: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Empty_Grass.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Empty_Grass.png')).resize((50, 50), Image.ANTIALIAS)),
            },
            BUILDING_FIRE: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Flame.jpeg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Flame.jpeg')).resize((50, 50), Image.ANTIALIAS)),
            },
            BUILDING_HOUSE: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'House.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'House.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
            BUILDING_KITCHEN: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Kitchen_Icon.jpg')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Kitchen_Icon.jpg')).resize((50, 50), Image.ANTIALIAS)),
            },
            BUILDING_PIT: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Pit_Icon.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Pit_Icon.png')).resize((50, 50), Image.ANTIALIAS)),},
            BUILDING_TREASURE: {
                'canvas': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Treasure_Chest.png')).resize((cell_width - 5, cell_height - 5), Image.ANTIALIAS)),
                'label': ImageTk.PhotoImage(Image.open(os.path.join(images_dir, 'Treasure_Chest.png')).resize((50, 50), Image.ANTIALIAS)),
            },
        }
        
    def UpdateLabels(self):
        # Decide if needs to level up
        while self.hero.xp >= (self.hero.level - 1) * 50 + 50:
            self.hero.xp = self.hero.xp - ((self.hero.level - 1) * 50 + 50)
            self.hero.level = self.hero.level + 1
            self.hero.hp = self.hero.hp + 50
            messagebox.showinfo(
                'Level Up!',
                'Hero gain +1 level up!\n +5 HP\nNow Hero is of Level %s' % self.hero.level)
        if self.hero.hp > (self.hero.level - 1) * 50 + 50:
            self.hero.hp = (self.hero.level - 1) * 50 + 50
            
        self.label_text_hero.set('%s: [XP %s/%s] [HP %s/%s] [Level %s]' % (
                self.hero.name,
                self.hero.xp, (self.hero.level - 1) * 50 + 50,
                self.hero.hp, (self.hero.level - 1) * 50 + 50,
                self.hero.level))
        m = self.mapdata.mapdata[self.hero.x][self.hero.y]
        print(str(m))
        if isinstance(m, Building):
            self.position_label.configure(
                image=self.building_images[m.building_type]['label'])
        else:
            self.position_label.configure(
                image=self.monster_images[m.subtype]['label'])
        self.label_text_position.set(m.LongStr())
        self.update_idletasks()
        if self.hero.hp <= 0:
            self.throwDiceToMoveBtn['state'] = 'disabled'
            self.hero.Reset()
        

    def HeroDoneMove(self, *args):
        x = self.hero.x
        y = self.hero.y
        if isinstance(self.mapdata.mapdata[x][y], Building):
            self.HandleHeroLandedOnBuilding(self.mapdata.mapdata[x][y])
        elif isinstance(self.mapdata.mapdata[x][y], Monster):
            self.HandleHeroLandedOnMonster(self.mapdata.mapdata[x][y])

    def HandleHeroLandedOnMonster(self, monster):
        monster_type = monster.subtype
        monster_data = MONSTER_DATA[monster_type]
        print('oh... landed on monster: ', monster_data['name'])
        will_fight = messagebox.askyesno(
            "Fight the monster?",
             "Hero landed on monster <%s [HP: %s] [Level: %s]>.\nDo you want to fight?" % (
                 monster_data['name'], monster_data['hp'], monster_data['lvl']
             )) 
        if will_fight:
            print('start fighting')
            r = random.random()
            if (r <= 0.75):
                # Hero wins
                self.hero.xp = self.hero.xp + monster_data['hp']
                messagebox.showinfo(
                    'Hero won!',
                    'Hero beats the monster, and gained %s XP' % monster_data['hp']
                )
            else:
                # Monster wins
                hit_lower_level = 1
                hit_upper_level = 12
                if monster.subtype in (MONSTER_HYDRA, MONSTER_WITHER, MONSTER_NEMEAN_LION):
                  hit_lower_level = 25
                  hit_upper_level = 36
                hp_damage = random.randint(hit_lower_level, hit_upper_level)
                self.hero.hp = self.hero.hp - hp_damage
                
                if self.hero.hp <= 0:
                    messagebox.showerror(
                        'Uho...',
                        'Hero recieved %s hit and died painfully.' % hp_damage
                    )
                else:
                    messagebox.showwarning(
                        'Phew...',
                        'Hero received %s hit but survived.' % hp_damage
                    )
        else:
            messagebox.showwarning('Coward....', 'The hero fled... what a shame!')
        print('hero data ', self.hero.xp)
        self.UpdateLabels()

    def HandleHeroLandedOnBuilding(self, building):
        b = BUILDING_DATA[building.building_type]
        if b['hp_impact'] == -math.inf:
            print('Hero died because all HP drained...')
            self.hero.hp = 0
            messagebox.showerror(
                'TRAGIC!!!',
                'Hero landed on %s and got all HP drained and died!' % b['name'])
            self.UpdateLabels()
            return
        self.hero.hp = self.hero.hp + b['hp_impact']
        self.hero.xp = self.hero.xp + b['xp_impact']
        if self.hero.hp <= 0:
            print('Hero died because HP gone...')
            messagebox.showerror(
                'SO SAD!',
                'Hero landed on %s and died!' % b['name'])
        else:
            messagebox.showinfo(
                'Oh...',
                'Hero landed on %s and gain %s XP and %s HP' % (
                    b['name'], b['xp_impact'], b['hp_impact']
                )
            )
        self.UpdateLabels()

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.mapdata = Map()
        self.mapdata.InitializeMap()
        self.mapdata.Print()
        self.hero = Hero(TYPE_HERO, HERO_WARRIOR)
        self.root = master
        self.pack()
        self.canvas = tk.Canvas(
            self, width=self.mapdata.width*50,
            height=self.mapdata.height*50, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.CreateWidgets()
        self.root.bind('<<HeroDoneMove>>', self.HeroDoneMove)
        self.first_time_rendering = True


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.master.title('Magic and Monsters')
    #app.master.maxsize(2000, 2000)
    app.mainloop()
    


main()