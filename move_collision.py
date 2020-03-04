import cocos
import math
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.actions import Driver
from cocos.director import director
import pyglet
from cocos.mapcolliders import RectMapCollider
from cocos.actions import Move
from pyglet.window import key
from cocos import layer
from pyglet.window import mouse

director.init(width=800, height=600, autoscale=False, resizable=True)
keyboard = key.KeyStateHandler()
target_x,target_y = (0,0)
rotation = 0


class BG(cocos.layer.Layer):
    def __init__(self,bg_name):
        super(BG,self).__init__()
        d_width, d_height = director.get_window_size()
        # 创建背景精灵
        background = cocos.sprite.Sprite(bg_name)
        background.position = d_width // 2, d_height // 2
        self.add(background)
start_bg = BG(bg_name="img/start.jpeg")  # 1.获取背景图片路径
class P_move(Action, RectMapCollider):
    def start(self):
        # We simply set the velocity of the target sprite to zero
        self.target.velocity = 0, 0

        # We also tell the game that our sprite is starting on the ground
        self.on_ground = True
    def on_bump_handler(self, vx, vy):
        return (vx, vy)

    def step(self,dt):
        x,y = self.target.position
        #self.target.rotation = 360-math.atan((target_y-y)/(target_x-x))*180
        #self.target.do(RotateBy(360,duration=1))
        self.target.do(MoveTo((target_x,target_y),duration=1))
        print(self.target.velocity)
        dx = self.target.velocity[0]
        dy = self.target.velocity[1]
        last_rect = self.target.get_rect()
        #print(last_rect)

        # Then we copy it into a new bounding rectangle that we can alter the values of to match what our math has done
        new_rect = last_rect.copy()

        # So we simply add our new X value to the old one (if it's moving left it will subtract instead)
        new_rect.x += dx

        # And we add our new Y value to the old one as well!
        new_rect.y += dy * dt
        # if (abs(math.atan((target_x-x)/(target_y-y)))*180
        #     if (x-target_x)>0:
        #         self.target.rotation += 0.5
        #     else:
        #         self.target.rotation -= 0.5
        # else:
        #     self.target.rotation = self.target.rotation
        print(self.target.rotation)
        self.target.speed = 100
        self.target.velocity = self.collide_map(start_bg, last_rect, new_rect, dy, dx)
        # self.target.speed = (math.sqrt(pow(target_x-x,2)+pow(target_y-y,2)))/5
        # self.target.velocity = ((target_x - x),(target_y-y))
        super(P_move, self).step(dt)
class MouseDisplay(cocos.layer.Layer):

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
        global target_x,target_y,rotation
        target_x,target_y = director.get_virtual_coordinates(x, y)
        rotation = math.atan((target_y-y)/(target_x-x))*180

class p_layer(layer.Layer):
    def __init__(self):
        super(p_layer, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite("img/car.png")

        # We set the position (standard stuff)
        self.sprite.position = 200, 500


        # Then we add it
        self.add(self.sprite)

        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        self.sprite.do(P_move())
p= p_layer()

main_pic_scence=cocos.scene.Scene(MouseDisplay())     #2.把背景图片生成scene
main_pic_scence.add(p)
director.window.push_handlers(keyboard)
director.run(main_pic_scence)