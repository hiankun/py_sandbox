"""This example is a clone of the using_sprites example with the difference 
that it uses pyglet instead of pygame to showcase sprite drawing. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math, random
import sys

import pyglet

import pymunk
from pymunk import Vec2d, BB
import pymunk.autogeometry

window = pyglet.window.Window(width=1024,height=768)

fps_display = pyglet.window.FPSDisplay(window)

logo_img = pyglet.resource.image('sp01_01.png')
logo_img.anchor_x = logo_img.width/2
logo_img.anchor_y = logo_img.height/2
logos = []
batch = pyglet.graphics.Batch()

### Physics stuff
space = pymunk.Space()
space.gravity = Vec2d(0.0, -90.0)

### Static line
static_lines = [
        pymunk.Segment(space.static_body, (11.0, 280.0), (407.0, 246.0), 0.0),
        pymunk.Segment(space.static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                ]
#shore_vs = [
#        (13 ,188),
#        (121 ,71),
#        (233 ,62),
#        (331 ,23),
#        (544 ,155),
#        (733 ,107),
#        (886 ,162),
#        (951 ,308),
#        (1017 ,351)
#        ]

for l in static_lines:
    l.friction = 0.5
space.add(static_lines)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        print(x,y)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        print('screenshot saved...')
        pyglet.image.get_buffer_manager().get_color_buffer().save(
                'save_using_sprites_pyglet.png')
    if symbol == pyglet.window.key.G:
        print('generate geometry...')
        generate_geometry(terrain_surface, space)

@window.event
def on_draw():
    window.clear()
    
    fps_display.draw()

    for line in static_lines:
        body = line.body
        
        pv1 = body.position + line.a.rotated(body.angle)
        pv2 = body.position + line.b.rotated(body.angle)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2f', (pv1.x,pv1.y,pv2.x,pv2.y)),
            ('c3f', (.8,.8,.8)*2)
            )
    batch.draw()
    
    #debug draw
    for logo_sprite in logos:
        
        ps = logo_sprite.shape.get_vertices()
        ps = [p.rotated(logo_sprite.body.angle) + logo_sprite.body.position for p in ps]
        n = len(ps)
        ps = [c for p in ps for c in p]
        
        pyglet.graphics.draw(n, pyglet.gl.GL_LINE_LOOP,
            ('v2f', ps),
            ('c3f', (1,0,0)*n)
            )
            
def update(dt):
    dt = 1.0/60. #override dt to keep physics simulation stable
    space.step(dt)
    
    for sprite in logos:
        # We need to rotate the image 180 degrees because we have y pointing 
        # up in pymunk coords.
        sprite.rotation = math.degrees(-sprite.body.angle) + 180
        #sprite.set_position(sprite.body.position.x, sprite.body.position.y)
        sprite.position = (sprite.body.position.x, sprite.body.position.y)
        
def spawn_logo(dt):
    x = random.randint(20,400)
    y = 500
    angle = random.random() * math.pi
    #vs = [(-23,26), (23,26), (0,-26)]
    w1 = 75
    w2 = 10
    w3 = 30
    h = 15
    vs = [(-w1,0), (-w3,h), (w2,h), (w1,0), (w2,-h), (-w3,-h)]
    mass = 10
    moment = pymunk.moment_for_poly(mass, vs)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Poly(body, vs)
    shape.friction = 2.0
    body.position = x, y
    body.angle = angle
    
    space.add(body, shape)
    
    sprite = pyglet.sprite.Sprite(logo_img, batch=batch)
    sprite.shape = shape
    sprite.body = body
    logos.append(sprite) 
    
def generate_geometry(surface, space):
    for s in space.shapes:
        if hasattr(s, "generated") and s.generated:
            space.remove(s)

    def sample_func(point):
        try:
            p = int(point.x), int(point.y)
            color = surface.get_at(p)
            return color.hsla[2] # use lightness
        except:
            return 0 

    line_set = pymunk.autogeometry.PolylineSet()
    def segment_func(v0, v1):
        line_set.collect_segment(v0, v1)
    
    pymunk.autogeometry.march_soft(
        BB(0,0,599,599), 60, 60, 90, segment_func, sample_func)

    for polyline in line_set:
        line = pymunk.autogeometry.simplify_curves(polyline, 1.)

        for i in range(len(line)-1):
            p1 = line[i]
            p2 = line[i+1]
            shape = pymunk.Segment(space.static_body, p1, p2, 1)
            shape.friction = .5
            shape.color = pygame.color.THECOLORS["red"]
            shape.generated = True
            space.add(shape) 


def main():
    pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.clock.schedule_once(spawn_logo, .1)
    pyglet.clock.schedule_interval(spawn_logo, 10/6.)
    pyglet.app.run()


if __name__ == '__main__':
    sys.exit(main())
