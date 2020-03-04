import cocos
import math
from cocos.actions import *
from cocos.sprite import Sprite
from cocos.actions import Driver
from cocos.director import director
import pyglet
from cocos.actions import Move
from pyglet.window import key
from cocos import layer
from pyglet.window import mouse
from cocos.collision_model import *

director.init(width=800, height=600, autoscale=False, resizable=True)
keyboard = key.KeyStateHandler()
target_x,target_y = (0,0)
collision_manager = CollisionManager()
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
        else:
            if dx > 0:
                self.angle = 180 - 180*math.atan(dx/-dy)/math.pi
            elif dx < 0:
                self.angle = 180 + 180*math.atan(-dx/-dy)/math.pi
            else:
                self.angle = self.angle
        self.target.do(MoveTo((target_x,target_y),duration = distance/self.target.speed)| RotateTo(self.angle,0))
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
        global target_x,target_y
        target_x,target_y = director.get_virtual_coordinates(x, y)
        
        

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
collision_manager.add(p)
# director.window.push_handlers(keyboard)
director.run(main_pic_scence)