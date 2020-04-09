import cocos
import pyglet
import math
from cocos.actions import *
from cocos.particle_systems import *
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.sprite import Sprite
from cocos import scenes
from pyglet.window import key
from cocos import layer
import cocos.collision_model as cm
from cocos.actions import Driver
from cocos.actions import Move
from pyglet.window import mouse
from cocos.collision_model import *
from cocos.skeleton import Bone, Skeleton
from cocos import skeleton
import root_bone
import root_skin
import animation
import animation.my_walk_skeleton
import animation.turn_my_walk_skeleton
import animation.turn_my_walk_skin
import animation.my_walk_skin
import animation.model1_skeleton
import animation.model1_skin
import animation.model2_skeleton
import animation.model2_skin
import animation.test_skeleton
import animation.test_skin
import _pickle as cPickle

address = "D:\MyCode\MyPython\BUPT_TowerDefence\img"
address_2 =  "D:\MyCode\MyPython\BUPT_TowerDefence"
# address = "D:\CSHE\BUPT_TowerDefence\img"
# address_2 = "D:\CSHE\BUPT_TowerDefence"
#address = "*****\BUPT_TowerDefence\img"
#address_2 = "***\BUPT_TowerDefence"

class MouseDisplay(cocos.layer.Layer):          #现在有bug 超出虚拟屏幕移动就有问题

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.text = cocos.text.Label('Mouse @', font_size=18,
                                     x=100, y=240)
        self.add(self.text)

    def on_mouse_motion(self, x, y, dx, dy):
        #dx,dy为向量,表示鼠标移动方向
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        #按下鼠标按键不仅更新鼠标位置,还改变标签的位置.这里使用director.get_virtual_coordinates(),用于保证即使窗口缩放过也能正确更新位置,如果直接用x,y会位置错乱,原因不明
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)
        self.text.element.x, self.text.element.y = director.get_virtual_coordinates(x, y)
        global target_x,target_y
        target_x,target_y = director.get_virtual_coordinates(x, y)

 
class Main_menu(cocos.menu.Menu):
    def __init__(self):
        super(Main_menu, self).__init__()

        items = []

        items.append(cocos.menu.ImageMenuItem('img/start.png',self.on_start))
        items.append(cocos.menu.ImageMenuItem('img/setting.png',self.on_setting))
        items.append(cocos.menu.ImageMenuItem('img/help.png',self.on_help))

        for i in items:
            i.x = 550

        self.create_menu(items,cocos.menu.shake(),cocos.menu.shake_back())


    def on_start(self):
        print("start")
        bg_2 = BG(bg_name="img/bg_2.png")
        scence_2=cocos.scene.Scene(bg_2)
        level_choose = Level_choose()
        scence_2.add(level_choose)
        director.replace(scenes.transitions.SlideInBTransition(scence_2, duration=1))

    def on_setting(self):
        print('setting')

    def on_help(self):
        print('help')

class MainLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        bg = cocos.sprite.Sprite("img/bg_3.jpg")
        bg.position = bg.width//2,bg.height//2

        self.px_width = bg.width
        self.px_height = bg.height

        self.mr_cai = Mr_cai()
        self.player = p_layer()
        self.life_bar=life_bar()
        self.enemy_num = 1

        self.spr1_layer = Sprite1()
        self.people_layer = PeopleLayer()
        self.bones = bone()
        fire = Fire()        #ParticleSystem
        fire.auto_remove_on_finish = True
        fire.position = (800,100)

        self.add(bg,0)
        self.add(fire,1)
        self.add(self.mr_cai,1)
        self.add(self.player,1)
        self.add(self.life_bar,2)
        self.add(self.spr1_layer,1)
        self.add(self.people_layer,1)
        self.add(self.bones,1)


class BG(cocos.layer.Layer):        #看是否需要传入background.position
    def __init__(self,bg_name):
        super(BG,self).__init__()
        d_width, d_height = director.get_window_size()
        # 创建背景精灵
        background = cocos.sprite.Sprite(bg_name)
        background.position = d_width // 2, d_height // 2
        self.add(background)
 

class Game_menu(cocos.menu.Menu):
    def __init__(self):
        super(Game_menu, self).__init__()

        items = []

        items.append(cocos.menu.ImageMenuItem('img/return.png',self.on_back))
        items.append(cocos.menu.ToggleMenuItem('Show FPS: ',self.on_show_fps,director.show_FPS))
        items.append(cocos.menu.ImageMenuItem('img/quit.png',self.on_quit))
        
        items[0].position = 250,-390
        items[1].position = -400,300
        items[2].position = 350,-300

        self.create_menu(items,cocos.menu.shake(),cocos.menu.shake_back())

    def on_back(self):         #有点Bug
        print("back")
        bg_2 = BG(bg_name="img/bg_2.png")
        scence_2=cocos.scene.Scene(bg_2)
        level_choose = Level_choose()
        scence_2.add(level_choose)
        director.replace(scenes.transitions.SlideInBTransition(scence_2, duration=1))

    def on_quit(self):
        director.window.close()

    def on_show_fps(self,show_fps):
        director.show_FPS = show_fps


class Level_choose(cocos.menu.Menu):
    def __init__(self):
        super(Level_choose, self).__init__()

        items = []

        items.append(cocos.menu.ImageMenuItem('img/level_1_icon.png',self.pic_1_callback))
        items.append(cocos.menu.ImageMenuItem('img/level_2_icon.png', self.pic_2_callback))
        
        items[0].position = 100,-110
        items[1].position = 300,-70

        self.create_menu(items,cocos.menu.zoom_in(),cocos.menu.zoom_out())
        self.count=0

    def pic_1_callback(self):
        print("第一关")
        #这次创建的窗口带调整大小的功能
        scene_3 = cocos.scene.Scene(MouseDisplay(),Game_menu())
        
        global block_1,block_1_R,block_2,block_3
        block_1 = False
        block_1_R = False
        block_2 = False
        block_3 = False
        global scroller
        scroller = cocos.layer.ScrollingManager()

        self.m_layer = MainLayer()
        self.player_1 = Player_1()
        # self.player_2 = Player_2()
        self.enemy_1 = Enemy_1()
        self.enemy_1_dead = False

        self.coll_manager = cm.CollisionManagerBruteForce()
        self.coll_manager.add(self.player_1)
        # self.coll_manager.add(self.player_2)
        self.coll_manager.add(self.enemy_1)
        self.coll_manager.add(self.player_1.bullet)

        scroller.add(self.m_layer)
        # scroller.add(self.player_2)
        scroller.add(self.enemy_1)
        scroller.add(self.player_1)

        # scene_3.schedule_interval(self.m_layer.update, 1 / 30)
        scene_3.schedule_interval(self.player_1.status_detect, 1 / 30)
        scene_3.schedule_interval(self.player_1.update_position, 1 / 80)
        # scene_3.schedule_interval(self.player_2.status_detect, 1 / 30)
        # scene_3.schedule_interval(self.player_2.update_position, 1 / 80)
        if not self.enemy_1_dead:
            scene_3.schedule_interval(self.enemy_1.update_position, 1 / 80)
            scene_3.schedule_interval(self.enemy_1.status_detect, 1 / 30)
        scene_3.schedule_interval(self.update, 1 / 80)
       
        scene_3.add(scroller,0)
        scene_3.add(MouseDisplay())

        director.replace(scenes.transitions.SlideInBTransition(scene_3, duration=1))

    def pic_2_callback(self):
        print("第二关")

    def update(self,dt):
        if not self.enemy_1_dead:
            if self.coll_manager.they_collide(self.player_1,self.enemy_1):
                block_1_R = True
                self.enemy_1.auto_attack = True
                if self.enemy_1.near_attack:
                    block_1 = True
                    if self.player_1.life < 2:
                        self.player_1.life = 0
                    else:
                        self.player_1.life -= 1
                        self.player_1.beheat = True
                else:
                    block_1 = False
            else:
                block_1_R = False
                block_1 = False
            if self.count!=0:
                self.count+=1
            if self.count>=7:
                self.count=0
            if self.coll_manager.they_collide(self.player_1.bullet,self.enemy_1):
                if self.count==0:
                    self.count+=1
                    self.player_1.count = 5 
                    if self.enemy_1.life <= 20:
                        self.enemy_1.life = 0
                        self.enemy_1_dead = True
                        scroller.remove(self.enemy_1)
                        del self.enemy_1
                    else:
                        self.enemy_1.life = self.enemy_1.life-5
                        self.enemy_1.beheat = True
        else:
            block_1_R = False
            block_1 = False


class P_move(Driver):
    def step(self,dt):
        x,y = self.target.position
        self.target.speed = 200
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(pow(dx,2) + pow(dy,2))
        if dy > 0 :
            if dx > 0:
                self.angle = 180*math.atan(dx/dy)/math.pi
            elif dx < 0:
                self.angle = 360 - 180*math.atan(-dx/dy)/math.pi
            else:
                self.angle = self.angle
        elif dy <0:
            if dx > 0:
                self.angle = 180 - 180*math.atan(dx/-dy)/math.pi
            elif dx < 0:
                self.angle = 180 + 180*math.atan(-dx/-dy)/math.pi
            else:
                self.angle = self.angle
        else:
            self.angle = self.angle
        self.target.do(MoveTo((target_x,target_y),duration = distance/self.target.speed)| RotateTo(self.angle,0))
        super(P_move, self).step(dt)

class p_layer(cocos.sprite.Sprite):
    def __init__(self):
        super(p_layer, self).__init__("img/car.png")
        self.position = 200, 500
        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)
        self.do(P_move())
    def stop(self):
        global target_x,target_y
        target_x,target_y= self.position

class draw_rec(cocos.layer.util_layers.ColorLayer):
    def __init__(self,w,h):
        super().__init__(255, 0,0,255,width =w,height=h)
        

class life_bar(cocos.sprite.Sprite):
    def __init__(self):
        super(life_bar, self).__init__("img/yellow_bar.png")


class Mover_1(cocos.actions.BoundedMove):
    def __init__(self):
        super().__init__(2300,1430)     #it should be bigger than the size of the picture  
    def step(self, dt):         #add block
        if not block_1:
            super().step(dt)
            vel_x = (keyboard[key.D] - keyboard[key.A])*400
            if block_1_R and vel_x > 0:
                vel_x = 0
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)
            global scroller
            scroller.set_focus(self.target.x,self.target.y)


class Mover_2(cocos.actions.BoundedMove):
    def __init__(self):
        super().__init__(2300,1430)     #it should be bigger than the size of the picture  
    def step(self, dt):         #add block
        if not block_2:
            super().step(dt)
            vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT])*400
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)
            # global scroller
            # scroller.set_focus(self.target.x,self.target.y)       #不能同时存在两个focus


class Mover_3(cocos.actions.BoundedMove):
    def __init__(self):
        super().__init__(2300,1430)     #it should be bigger than the size of the picture  
    def step(self, dt):         #add block
        if not block_3:
            super().step(dt)
            vel_x = -100
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)
            

class Sprite1(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(address+"/man.png")
        img_grid = pyglet.image.ImageGrid(img,1,4,item_width=100,item_height = 100)     #1row 4col each one is 100*100


        anim = pyglet.image.Animation.from_image_sequence(img_grid[0:],0.2,loop = True) #define the range of the photo and the second parameter is to descibe the period

        spr = cocos.sprite.Sprite(anim)
        spr.position = 200,500
        self.add(spr)


class PeopleLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(address+"\girl.png")

        img_grid = pyglet.image.ImageGrid(img,4,8,item_width = 120,item_height=150)

        anim = pyglet.image.Animation.from_image_sequence(img_grid,0.1,loop = True)

        spr = cocos.sprite.Sprite(anim)
        spr.position = 640,500

        self.add(spr)      


class Mr_cai(cocos.layer.ScrollableLayer):
    def __init__(self):
        super( Mr_cai, self ).__init__()

        x,y = director.get_window_size()
        self.skin = skeleton.BitmapSkin(animation.model1_skeleton.skeleton, animation.model1_skin.skin)
        self.add( self.skin )
        x, y = director.get_window_size()
        self.skin.position = 300, 150
        fp0 = open((address_2+"/animation/Mr_cai.anim"),"rb+")
        anim = cPickle.load(fp0)
        self.skin.do( cocos.actions.Repeat( skeleton.Animate(anim) ) )


class Player_1(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(Player_1, self).__init__()
        # self.do(Repeat(MoveTo((600, 200), 5) + MoveTo((100, 200), 5)))
        self.skin = skeleton.BitmapSkin(animation.model2_skeleton.skeleton, animation.model2_skin.skin)
        self.add(self.skin)

        # self.width,self.height = 0,0        #可能有bug
        self.position = 100,100
        self.skin.position = 100, 100
        self.life = 100

        img = pyglet.image.load(address+"\dot.png")
        self.spr = cocos.sprite.Sprite(img,opacity=0)
        self.spr.position = 100,100
        self.spr.velocity = (0,0)
        self.spr.do(Mover_1())
        self.add(self.spr)
        self.life_bar = life_bar()
        self.add(self.life_bar)

        self.status = 3 #1:walk left 2:walk right 3:stop 4:attack
        self.change = False
        self.block = False #True means the character is having a continuous movement
        self.count = 0
        self.beheat = False

        global block_1

        fp_1 = open((address_2 + "/animation/MOOOOVE1.anim"), "rb+")
        self.walk = cPickle.load(fp_1)

        fp_2 = open((address_2 + "/animation/gun_shot.anim"), "rb+")
        self.attack = cPickle.load(fp_2)

        fp_3= open((address_2+"/animation/my_frozen.anim"),"rb+")
        self.frozen = cPickle.load(fp_3)

        # self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)
        self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position),65,136)

        self.fire()
        self.bullet.cshape = cm.AARectShape(eu.Vector2(*self.bullet.position),self.bullet.width/2,self.bullet.height/2)


    def remove_all(self):
        if len(self.skin.actions) > 0:
            for i in range(0,len((self.skin.actions))):          
                self.skin.remove_action(self.skin.actions[0])


    def update_position(self,dt):
        if not block_1:
            self.skin.position = self.spr.position  #!!!!!!! self.position = -(self.skin.position-600)
            x,y = self.skin.position
            self.life_bar.position = (x, y+160)
            self.life_bar.scale_x = self.life/100
            self.cshape.center = eu.Vector2(*self.skin.position)
            self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)

    def fire(self):             #有个bug
        self.bullet = cocos.sprite.Sprite("img/bullet.png")
        # x,y = self.skin.position
        self.bullet.position = -100, -100   #初始在屏幕外

        self.add(self.bullet)

    def status_detect(self, dt):
        self.bullet.cshape.center = self.bullet.position
        if self.block:
            if self.count <= 4:
                self.count += 1
                x,y = self.bullet.position
                self.bullet.position = x+40, y
            else:
                self.count = 0
                self.bullet.position = -100,-100
                self.block = False
                global block_1
                block_1 = self.block
        else:
            if (keyboard[key.J]):
                if self.status != 4:
                    self.remove_all()
                    self.status = 4
                    self.change = True
                else:
                    self.change = False
                    x,y = self.skin.position
                    self.bullet.position = x+110, y+70
                    self.block = True
                    block_1 = self.block
            elif (keyboard[key.D]):      #key right and not attack
                if self.status != 2 and self.status != 1:
                    self.remove_all()
                    self.status = 2
                    self.change = True
                else:
                    self.change = False
            elif (keyboard[key.A] and not block_1_R):      #key right and not attack
                if self.status != 1:
                    self.remove_all()
                    self.status = 1
                    self.change = True
                else:
                    self.change = False
            elif self.beheat:
                self.remove_all()
                self.status = 3
                self.beheat = False
                self.block = True
                block_3 = self.block
                self.skin.do(skeleton.Animate(self.frozen))
            else:
                self.remove_all()
                if self.status != 3:
                    self.status = 3
                    self.change = True
                else:
                    self.change = False
        if self.change:
            if self.status == 1:
                self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
            else:
                if self.status == 2:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
                elif self.status == 4:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.attack)))           #there is a bug:return attack
                    x,y = self.skin.position
                    self.bullet.position = x+110,y+70   #并没有重复
                    # self.fire()
                    self.block = True
                    block_1 = self.block
            self.change = False


class Player_2(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(Player_2, self).__init__()
        # self.do(Repeat(MoveTo((600, 200), 5) + MoveTo((100, 200), 5)))
        self.skin = skeleton.BitmapSkin(animation.my_walk_skeleton.skeleton, animation.my_walk_skin.skin)
        self.add(self.skin)

        self.skin.position = 500, 100
        self.position = 500,100
        self.life = 100

        img = pyglet.image.load(address+"\dot.png")
        self.spr = cocos.sprite.Sprite(img,opacity=0)       #hide the dot
        self.spr.position = 500,100
        self.spr.velocity = (0,0)
        self.spr.do(Mover_2())
        self.life_bar = life_bar()

        self.add(self.spr)
        self.add(self.life_bar)

        self.status = 3 #1:walk left 2:walk right 3:stop 4:attack
        self.change = False
        self.block = False #True means the character is having a continuous movement
        self.near_attack = False
        self.count = 0

        self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position),65,136)#136不够

        fp_1 = open((address_2 + "/animation/MOOOOVE.anim"), "rb+")
        self.walk = cPickle.load(fp_1)

        fp_2= open((address_2+"/animation/attack.anim"),"rb+")
        self.attack = cPickle.load(fp_2)

        
    def remove_all(self):
        if len(self.skin.actions) > 0:
            for i in range(0,len((self.skin.actions))):          
                self.skin.remove_action(self.skin.actions[0])

    def update_position(self,dt):
        if not block_2:
            self.skin.position = self.spr.position
            x,y = self.skin.position
            self.life_bar.position = (x, y+160)
            self.life_bar.scale_x = self.life/100
            self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)
        
    def status_detect(self, dt):
        self.cshape.center = eu.Vector2(*self.skin.position)         #优化其放置位置
        if self.block:
            if self.count <= 5:
                self.count += 1
                self.near_attack = True
            else:
                self.count = 0
                self.near_attack = False
                self.block = False
                global block_2
                block_2 = self.block
        else:
            if (keyboard[key.NUM_1]):
                if self.status != 4:
                    self.remove_all()
                    self.status = 4
                    self.change = True
                else:
                    self.change = False
                    self.block = True
                    block_2 = self.block
            elif (keyboard[key.RIGHT]):      #key right and not attack
                if self.status != 2 and self.status != 1:
                    self.remove_all()
                    self.status = 2
                    self.change = True
                else:
                    self.change = False
            elif (keyboard[key.LEFT]):      #key right and not attack
                if self.status != 1:
                    self.remove_all()
                    self.status = 1
                    self.change = True
                else:
                    self.change = False
            else:
                self.remove_all()
                if self.status != 3:
                    self.status = 3
                    self.change = True
                else:
                    self.change = False
        if self.change:
            if self.status == 1:
                self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
            else:
                if self.status == 2:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
                elif self.status == 4:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.attack)))           #there is a bug:return attack
                    self.block = True
                    block_2 = self.block
            self.change = False


class Enemy_1(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(Enemy_1, self).__init__()
        self.skin = skeleton.BitmapSkin(animation.test_skeleton.skeleton, animation.test_skin.skin)
        self.add(self.skin)

        self.skin.position = 700, 60
        self.position = self.skin.position
        self.life = 100

        img = pyglet.image.load(address+"\dot.png")
        self.spr = cocos.sprite.Sprite(img,opacity=0)       #hide the dot
        self.spr.position = self.skin.position
        self.spr.velocity = (0,0)
        self.spr.do(Mover_3())
        self.life_bar = life_bar()

        self.add(self.spr)
        self.add(self.life_bar)

        self.status = 3 #1:walk left 2:walk right 3:stop 4:attack 5：beheat
        self.change = False
        self.block = False #True means the character is having a continuous movement
        self.near_attack = False
        self.auto_attack = False
        self.dead = False
        self.count = 0
        self.beheat = False

        self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position),65,136)#136不够

        fp_1 = open((address_2 + "/animation/2t.anim"), "rb+")
        self.walk = cPickle.load(fp_1)

        fp_2= open((address_2+"/animation/E_attack.anim"),"rb+")
        self.attack = cPickle.load(fp_2)

        fp_3= open((address_2+"/animation/frozen.anim"),"rb+")
        self.frozen = cPickle.load(fp_3)
        
    def remove_all(self):
        if len(self.skin.actions) > 0:
            for i in range(0,len((self.skin.actions))):          
                self.skin.remove_action(self.skin.actions[0])

    def update_position(self,dt):
        if not block_3:
            self.skin.position = self.spr.position
            x,y = self.skin.position
            self.life_bar.position = (x, y+160)
            self.life_bar.scale_x = self.life/100
            self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)
        
    def status_detect(self, dt):
        if self.life > 0:
            self.cshape.center = eu.Vector2(*self.skin.position)         #优化其放置位置
            if self.beheat:
                self.remove_all()
                self.beheat = False
                self.status = 5
                self.block = True
                global block_3
                block_3 = self.block
                self.skin.do(skeleton.Animate(self.frozen))
            if self.block:
                if self.count <= 8:
                    self.count += 1
                    self.near_attack = True
                elif self.count > 8 and self.count <= 15:           #砍完的延迟
                    self.count += 1
                    self.near_attack = False
                    self.status = 3
                    self.remove_all()
                else:
                    self.count = 0
                    # self.near_attack = False
                    self.block = False
                    block_3 = self.block
                    self.auto_attack = False
            else:
                if self.auto_attack:
                    if self.status != 4:
                        self.remove_all()
                        self.status = 4
                        self.change = True
                    else:
                        self.change = False
                        self.block = True
                        block_3 = self.block
                else:
                    if self.status != 1:
                        self.remove_all()
                        self.status = 1
                        self.change = True
                    else:
                        self.change = False
            if self.change:
                if self.status == 1 or self.status == 2:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
                elif self.status == 4:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.attack)))           #there is a bug:return attack
                    self.block = True
                    block_3 = self.block
                self.change = False
        else:
            block_3 = True
            self.remove_all()




class bone(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(bone,self).__init__()

        x,y = director.get_window_size()

        self.skin = cocos.skeleton.BitmapSkin(root_bone.skeleton,root_skin.skin)

        
        self.add(self.skin)
        self.skin.position = 300,500


class BackgroundLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        bg = cocos.sprite.Sprite("img/bg_3.jpg")

        bg.position = bg.width//2,bg.height//2

        self.px_width = bg.width
        self.px_height = bg.height

        self.add(bg)


if __name__=='__main__':
    #全局变量
    target_x,target_y = (0,0)
    block_1 = False
    block_1_R = False
    block_2 = False
    block_3 = False
    #初始化导演
    director.init(width=1201,height=686,caption="BUPT Tower Defence")
    director.window.pop_handlers()
    #键盘
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    bg_1 = BG(bg_name="img/start_bg.png")           #1.获取背景图片路径
    scene_1=cocos.scene.Scene(bg_1)     #2.把背景图片生成scene
    scene_1_menu = Main_menu()
    scene_1.add(scene_1_menu)                #4.把按钮加入到scene
    director.run(scene_1)    #5.启动场景