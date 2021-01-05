from stdproyectlib import *
import pyglet as pg
from math import pi

win = pg.window.Window(fullscreen=True, resizable=True, caption="vector-3D")
batch = pg.graphics.Batch()
ptos = [
    vector(0,0,0),
    vector(0,0,1),
    vector(0,1,0),
    vector(0,1,1),
    vector(1,0,0),
    vector(1,0,1),
    vector(1,1,0),
    vector(1,1,1),
]
ln = [
    [0,1],
    [0,2],
    [0,4],
    [1,5],
    [1,3],
    [2,3],
    [2,6],
    [3,7],
    [4,5],
    [4,6],
    [5,7],
    [6,7],
]
cube = obj3D(batch,win.width,win.height,ptos,ln,vector(0,0,10))
cubeRot = obj3D(batch,win.width,win.height,ptos,ln,vector(3,0,10))
cube0 = obj3D(batch,win.width,win.height,ptos,ln,vector(0,0,-10))
cube1 = obj3D(batch,win.width,win.height,ptos,ln,vector(50,50,-25))
cube2 = obj3D(batch,win.width,win.height,ptos,ln,vector(40,0,-10))
cam = camera(vector(0,45,0),FOV=1000)
cam.abs_rot(-pi/2,0,0)
count=0
Vk_j,Vk_i,Vj_i = 0,0,0
Vi,Vj,Vk = 0,0,0
t=0
def update(dt):
    global count,k_vector,t
    t+=dt
    if count<2:
        count+=1
        return None
    cubeRot.dnr_dtn[0].x -= 3*sin(t)*dt
    cubeRot.dnr_dtn[0].y += 3*cos(t)*dt
    cam.rel_rot(Vk_j*dt,Vk_i*dt,Vj_i*dt)
    cam.r += (Vi*cam.i + Vj*cam.j + Vk*cam.k)*dt
pg.clock.schedule_interval(update,1/60)


@win.event
def on_draw():
    win.clear()
    render(cube,cam)
    render(cubeRot,cam)
    render(cube0,cam)
    render(cube1,cam)
    render(cube2,cam)
    batch.draw()

@win.event
def on_key_press(symbol,modifiers):
    global Vk_j,Vk_i,Vj_i, Vi,Vj,Vk
    if symbol==pg.window.key.J:
        Vk_i = -1
    if symbol==pg.window.key.K:
        Vk_j = -1
    if symbol==pg.window.key.L:
        Vk_i =  1
    if symbol==pg.window.key.U:
        Vj_i = -1
    if symbol==pg.window.key.I:
        Vk_j =  1
    if symbol==pg.window.key.O:
        Vj_i =  1

    if symbol==pg.window.key.A:
        Vi = -5
    if symbol==pg.window.key.S:
        Vk = -5
    if symbol==pg.window.key.D:
        Vi =  5
    if symbol==pg.window.key.R:
        Vj =  5
    if symbol==pg.window.key.W:
        Vk =  5
    if symbol==pg.window.key.F:
        Vj = -5

@win.event
def on_key_release(symbol,modifiers):
    global Vk_j,Vk_i,Vj_i, Vi,Vj,Vk
    if symbol==pg.window.key.J:
        Vk_i = 0
    if symbol==pg.window.key.K:
        Vk_j = 0
    if symbol==pg.window.key.L:
        Vk_i = 0
    if symbol==pg.window.key.U:
        Vj_i = 0
    if symbol==pg.window.key.I:
        Vk_j = 0
    if symbol==pg.window.key.O:
        Vj_i = 0

    if symbol==pg.window.key.A:
        Vi = 0
    if symbol==pg.window.key.S:
        Vk = 0
    if symbol==pg.window.key.D:
        Vi = 0
    if symbol==pg.window.key.R:
        Vj = 0
    if symbol==pg.window.key.W:
        Vk = 0
    if symbol==pg.window.key.F:
        Vj = 0
pg.app.run()