import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import pygame
from pygame.locals import *
import pymunk.constraints


pygame.init()
width, height= 1000,800
window=pygame.display.set_mode((width, height))
space = pymunk.Space()

class PivotJoint:
    def __init__(self, b, b2, a=(0, 0), a2=(0, 0), collide=True):
        joint = pymunk.constraints.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        space.add(joint)
        
class SimpleMotor:
    def __init__(self, b, b2, rate):
        joint = pymunk.constraints.SimpleMotor(b, b2, rate)
        space.add(joint)


def draw(space, window, draw_options):
    window.fill('white')
    space.debug_draw(draw_options)
    pygame.display.update()
    


def pedal(space):
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (200, 300)
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = (200, 300)
    line = pymunk.Poly.create_box(body,(50, 200))
    line.friction = 1
    line.mass = 8
    box=pymunk.Poly(body,[(-50,25), (-20,25), (-20,150), (-50,150)])
    box.friction=1
    box.mass=8
    space.add(line, box, body)
    
def pipe(space):
    rects = [[(475, 300), (400, 10)], [(475, 350), (400, 10)],
             [(575, 310), (200, 10)], [(575, 340), (200, 10)],
          [(675, 250), (10, 100)], [(675, 400),(10, 100)],
           [(725, 325), (10, 250)], [(50, 200), (800, 10)], 
           [(50, 450), (800, 10)]] #, [(715, 325), (10, 100)]
        
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.5
        shape.friction = 0.0
        space.add(body, shape)
        
def break_Left(space):
    body = pymunk.Body()
    body.position = (687.5,200)
    line = pymunk.Poly.create_box(body,(200, 20), radius=1)
    line.friction = 0.9
    line.mass = 20
    box=pymunk.Poly(body,[(-20,10), (20,10), (20,120), (-20,120)])
    space.add(body, line, box)
    
def break_Right(space):
    body = pymunk.Body()
    body.position = (687.5,450)
    line = pymunk.Poly.create_box(body,(200, 20), radius = 1)
    line.friction = 0.9
    line.mass = 20
    box = pymunk.Poly(body, [(-20,-10), (20,-10), (20,-120), (-20,-120)])
    space.add(body, line, box)
    
def break_Center(space):
    body = pymunk.Body()
    body.position = (250, 325)
    line = pymunk.Poly.create_box(body, (20, 200), radius=1)
    line.friction = 1
    line.mass = 30
    box = pymunk.Poly(body, [(110,20), (110,-20), (10,-20), (10,20)])
    space.add(body, line, box)
    
def create_ball(space):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position=(500, 325)
    shape = pymunk.Circle(body, 3)
    shape.mass = 0.1
    shape.elasticity = 0.2
    shape.friction = 0.0
    shape.color = (255,0,0,100)
    space.add(body, shape)
    
def create_wheel_R(space):
    body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
    body.position = (700, 535)
    shape  =pymunk.Circle(body, 60)
    shape.mass = 30
    shape.elasticity = 0.0
    shape.friction = 0.9
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (700,535)
    PivotJoint(body, rotation_center_body,(0,0))
    shape.color = (0,255,0,100)
    space.add(body, shape)
    return shape
    
def create_wheel_L(space):
    body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
    body.position = (700, 115)
    shape = pymunk.Circle(body, 60)
    shape.mass = 30
    shape.elasticity = 0.9
    shape.friction = 0.9
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (700,115)
    PivotJoint(body, rotation_center_body, (0,0))
    shape.color=(0, 255, 0, 100)
    space.add(body, shape)
    return shape
    
    

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 4/fps
    
    #space = pymunk.Space()
    space.gravity = (0, 0)
    pedal(space)
    pipe(space)
    break_Right(space)
    break_Left(space)
    break_Center(space)
    
    wheel=create_wheel_R(space)
    wheel.body.apply_impulse_at_local_point((-1500, 0), (0,60))
    
    wheel2=create_wheel_L(space)
    wheel2.body.apply_impulse_at_local_point((-1500, 0), (0,60))
    
    for i in range(360):
        create_ball(space)
        
    
    active_shape = None
    
    
    draw_options = pymunk.pygame_util.DrawOptions(window)
    pressed_paused = None
    
    while run:
        
        
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run= False
                break  
                
        ## FIRST CLICK THE PEDAL, AND THEN USE THE RIGHT AND LEFT ARROW KEYS
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = from_pygame(event.pos, window)
                active_shape = None
                for s in space.shapes:
                    if s.point_query(p).distance < 0:
                        active_shape = s
                        
                        
            keys = {K_LEFT: (-1, 0), K_RIGHT: (1, 0)}
                        
            if event.type == KEYDOWN: 
                if event.key in keys:
                    active_shape.body.body_type = pymunk.Body.DYNAMIC
                    x, y = keys[event.key]
                    v = Vec2d(x, y)*10
                    
                    if active_shape != None:
                        active_shape.body.position += v
            else:
                try:
                    active_shape.body.body_type=pymunk.Body.STATIC
                except:
                    active_shape=None
                
            
                                     
            
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)
    pygame.quit()
    
if __name__ == '__main__':
    run(window, width, height)
