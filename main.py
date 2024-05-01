from kivy.app import App, runTouchApp
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.carousel import Carousel
from kivy.uix.effectwidget import*
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.graphics.context_instructions import PopMatrix, PushMatrix, Rotate
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from random import randint as rand, random
import math
try:
    import keyboard
except:pass
try:
    import pretty_errors
except:pass
def txt_to_texture(text = "text", font = 30, color = (1,1,1,1)):
    #Возващает [0] = texture; [1] = texture_size
    mylbl = CoreLabel(text = text, font_size = font, color = color)
    mylbl.refresh()
    return mylbl.texture, list(mylbl.texture.size)
class coliders:
    #Этот отрывок кода тебя ебать не должен!
    def __init__(self, x,y,width,height):
        self.pos = x,y
        self.size = width, height
def physic_engine(a, b_returning, last_position, set_rot = None, max_otklon = None, max_speed = None, func_otkl = None):
    #Этот отрывок кода тебя ебать не должен!
    if not is_touching(a, b_returning):save.lt = False; return False
    b_l=b_returning.pos[0]
    b_r=b_returning.pos[0] + b_returning.size[0]
    b_b=b_returning.pos[1]
    b_t=b_returning.pos[1] + b_returning.size[1]
    result=[]
    width= b_returning.pos[0] - b_returning.pos[0] + b_returning.size[0]
    height=b_returning.pos[1] - b_returning.pos[1] + b_returning.size[1]
    x=b_returning.pos[0]
    y=b_returning.pos[1]
    t = coliders(x=x,y=b_t,width=width,height=1)
    b = coliders(x=x,y=b_b,width=width,height=1)
    r = coliders(x=b_r,y=y+1,width=1,height=height-2)
    l = coliders(x=b_l,y=y+1,width=1,height=height-2)
    sp = list(last_position)
    while is_touching(a, b_returning):
        if is_touching(a, l): sp[0] = last_position[0] - 1
        elif is_touching(a, r): sp[0] = last_position[0] + 1
        elif is_touching(a, t): sp[1] = last_position[1] + 1
        elif is_touching(a, b): sp[1] = last_position[1] - 1
        a.pos=tuple(sp)
    if a.rot.angle > max_otklon and a.rot.angle < 360 - max_otklon:
        func_otkl()
    if not max_speed and not save.lt:
        func_otkl()
    if set_rot != None:
        a.rot.angle = 0
    save.lt = True
    return True
def is_touching(a,b):
    a_l=a.pos[0]
    a_r=a.pos[0] + a.size[0]
    a_b=a.pos[1]
    a_t=a.pos[1] + a.size[1]
    b_l=b.pos[0]
    b_r=b.pos[0] + b.size[0]
    b_b=b.pos[1]
    b_t=b.pos[1] + b.size[1]
    if a_l >= b_r or a_r <= b_l or a_t <= b_b or a_b >= b_t: return False
    return True
def camera_move(a,objs):#Фокусит камеру на игроке
    prop = Window.width, Window.height
    d = a.pos[0] * -1 + prop[0]/2 - a.size[0]/2, a.pos[1] * -1 + prop[1]/2 - a.size[1]/2
    for i in objs:
        i = objs[i]
        c = [i.pos[0] + d[0], i.pos[1] + d[1]]
        i.pos = c
def move(obj, steps, _angle):
    angle = math.radians(_angle)
    obj.pos[0] += steps * math.cos(angle)
    obj.pos[1] += steps * math.sin(angle)
    return steps * math.cos(angle), steps * math.sin(angle)
class ImageButton(Button):
    def __init__(self, Image, size = (170,170), **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.background_normal = Image
        self.background_down   = Image
        self.size = size
        self.size_hint = (None, None)
Window.clearcolor = (.3, .91, .85, 1)
class Helicopter(Image):
    def __init__(self, size = [100,100], source = None, **kwargs ):
        super(Helicopter, self ).__init__( **kwargs )
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle  = 0
            self.rot.origin = self.center
            self.rot.axis = (0, 0, 1)
        with self.canvas.after:
            PopMatrix()
        self.state_mirror = 0
        self.size_hint = (None, None)  # tell the layout not to size me
        self.img    = source
        self.source    = self.img
        self.size      = size
        self.rot.origin = self.center # Reset the center of the Rotate canvas instruction
    def update_img(self):
        self.source    = self.img
class pr:
    def __init__(self):#Суём "глобальные" переменные
        self.lt = False
        self.game = False
        self.prop = Window.width, Window.height
        self.BackFlipButton = False
        self.MirrorButton = False
        self.ForwFlipButton = False
        self.Урвв = False
        self.Нар = False
        self.Урвп = False
        self.real_gaz = 0
        self.РШГ = 0
        self.use_cycle = False
        self.Mirror_complite = False
        self.num_img = 0
save = pr()
class lvl1(Widget):
    def __init__(self, **kv):
        super(lvl1, self).__init__(**kv)
        self.o = {}#Объекты
        with self.canvas:
            self.o["floor0"] = Rectangle(pos =(-300,0),size = (1500, 500), source = "grass.png")
            self.o["floor1"]= Rectangle(pos=(1200,0),size = (1500, 500), source = "grass.png")
            self.o["floor2"]= Rectangle(pos=(2700,0),size = (1500, 500), source = "grass.png")
            self.o["floor3"]= Rectangle(pos=(2700 + 1500,0),size = (1500, 500), source = "grass.png")
            Color(.5,.5,.5,1)
            self.o["stone"] = Rectangle(pos = (-1300, 0) ,size = (1000,20000))
            Color(1,1,1,1)
            self.o["heli" ] =Helicopter(pos = [100, 600],size = [160, 90],source = "Ka_50_0.png")
            self.o["grass"] = coliders(-300, -22, 5700, 500)
            self.o["stone collider"] = coliders(-1300, 0, 1000, 100000)
        if not save.use_cycle:
            Clock.schedule_interval(self.cycle, 1/60)
            save.use_cycle = True
        
    def fliping(self, q = None):
        if save.MirrorButton and not save.Mirror_complite:
            x.MirrorButton.disabled = True
            save.num_img += 1
            self.o["heli"].img = f"Ka_50_{save.num_img}.png"
            self.o["heli"].update_img()
            if save.num_img > 3:
                save.Mirror_complite = True
                x.MirrorButton.disabled = False
            else:
                Clock.schedule_once(self.fliping, .3)
        elif not save.MirrorButton and save.Mirror_complite:
            x.MirrorButton.disabled = True
            save.num_img -= 1
            self.o["heli"].img = f"Ka_50_{save.num_img}.png"
            self.o["heli"].update_img()
            if save.num_img < 1:
                save.Mirror_complite = False
                x.MirrorButton.disabled = False
            else:
                Clock.schedule_once(self.fliping, .3)

    def cycle(self, q = None):
        lp = self.o["heli"].pos
        x.height_heli.text = str(int(self.o["heli"].pos[1] - (self.o["grass"].pos[1]+500)))[:-1] + "m"
        self.o["heli"].rot.origin = self.center
        save.real_gaz += rand(-1,1) / 60
        if save.real_gaz == save.РШГ:
            pass
        elif save.real_gaz < save.РШГ:
            save.real_gaz += .045
        else:
            save.real_gaz -= .07
        if save.BackFlipButton:
            self.o["heli"].rot.angle += 1
        elif save.ForwFlipButton:
            self.o["heli"].rot.angle -= 1
        try:
            if keyboard.is_pressed("a"):
                self.o["heli"].rot.angle += 1
            if keyboard.is_pressed("d"):
                self.o["heli"].rot.angle -= 1
        except:pass
        if self.o["heli"].rot.angle < 0:
            self.o["heli"].rot.angle += 360
        elif self.o["heli"].rot.angle >= 360:
            self.o["heli"].rot.angle -= 360
        move(self.o["heli"], -20, 90)
        move(self.o["heli"], save.real_gaz + 20, self.o["heli"].rot.angle + 90)
        physic_engine(self.o["heli"], self.o["grass"], lp, 0, 18, save.РШГ > -3, self.clear_canv)
        if is_touching(self.o["heli"], self.o["stone collider"]):
            self.clear_canv()
        camera_move(self.o["heli"], self.o)
    def clear_canv(self):
        self.canvas.clear()
        save.game = False
        save.prop = Window.width, Window.height
        save.BackFlipButton = False
        save.MirrorButton = False
        save.ForwFlipButton = False
        x.MirrorButton.disabled = False
        save.Урвв = False
        save.Нар = False
        save.Урвп = False
        save.real_gaz = 0
        save.РШГ = 0
        self.__init__()
class app(App):
    def build(self):
        lay1 = FloatLayout()
        self.x2 = lvl1()
        lay1.add_widget(self.x2)
        BackFlipButton = ImageButton("left.png")
        self.MirrorButton   = ImageButton("Ka_50_2.png", (300, 170))
        ForwFlipButton = ImageButton("right.png")
        Урвв           = ImageButton("VV.png")
        Нар            = ImageButton("HAP.png")
        Урвп           = ImageButton("Vll.png")
        self.РШГ = Slider(min = -10, max = 2, value = 0, orientation = 'vertical', value_track = True,value_track_color=(1, 0, 0, 1),value_track_width = 15)
        lay = GridLayout(rows = 1)
        lay.add_widget(BackFlipButton)
        lay.add_widget(self.MirrorButton)
        lay.add_widget(ForwFlipButton)
        lay.add_widget(Label())
        self.height_heli = Label(color = (.3,0,0,1))
        self.height_heli.y = save.prop[1]-150
        lay.add_widget(self.height_heli)
        lay.add_widget(Урвв)
        lay.add_widget(Нар)
        lay.add_widget(Урвп)
        lay.add_widget(self.РШГ)
        lay1.add_widget(lay)
        BackFlipButton.on_press   = self.BackFlipButton_t
        BackFlipButton.on_release = self.BackFlipButton_f
        self.MirrorButton.on_release   = self.MirrorButton_func
        ForwFlipButton.on_press   = self.ForwFlipButton_t
        ForwFlipButton.on_release = self.ForwFlipButton_f
        Урвв.on_press             = self.Урвв_t
        Урвв.on_release           = self.Урвв_f
        Урвв.on_press             = self.Урвп_t
        Урвв.on_release           = self.Урвп_f
        Нар.on_press              = self.Нар_t
        Нар.on_release            = self.Нар_f
        Clock.schedule_interval(self.cycle, .1)
        return lay1
    def BackFlipButton_f(self):
        save.BackFlipButton = False
    def BackFlipButton_t(self):
        save.BackFlipButton = True
    def MirrorButton_func(self):
        if save.MirrorButton:
            save.MirrorButton = False
        else:
            save.MirrorButton = True
        Clock.schedule_once(x.x2.fliping, .2)
    def ForwFlipButton_f(self):
        save.ForwFlipButton = False
    def ForwFlipButton_t(self):
        save.ForwFlipButton = True
    def Урвв_f(self):
        save.Урвв = False
    def Урвв_t(self):
        save.Урвв = True
    def Нар_t(self):
        save.Нар = True
    def Нар_f(self):
        save.Нар = False
    def Урвп_t(self):
        save.Урвп = True
    def Урвп_f(self):
        save.Урвп = False
    def cycle(self, x=None):
        if self.РШГ.value >= 0:
            self.РШГ.value_track_color = (0,1,0,1)
        else:
            self.РШГ.value_track_color = (1,0,0,1)
        try:
            if keyboard.is_pressed("w"):
                self.РШГ.value += 1
            elif keyboard.is_pressed("s"):
                self.РШГ.value -= 1
        except Exception as E: print(E)
        while self.РШГ.value < self.РШГ.min:
            self.РШГ.value = self.РШГ.min
        while self.РШГ.value > self.РШГ.max:
            self.РШГ.value = self.РШГ.max
        save.РШГ = self.РШГ.value
if __name__ == "__main__":
    x = app()
    x.run()