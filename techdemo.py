from stdproyectlib import *
import pyglet as pg
from math import pi

win = pg.window.Window(fullscreen=True, resizable=True, caption="vector-3D")
batch = pg.graphics.Batch()
ptos = [
    vector(-1,-1,-1),
    vector(-1,-1, 1),
    vector(-1, 1,-1),
    vector(-1, 1, 1),
    vector( 1,-1,-1),
    vector( 1,-1, 1),
    vector( 1, 1,-1),
    vector( 1, 1, 1),
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


cube_grid = [obj3D(batch,win.width,win.height,ptos,ln,m*0.1,0,0,vector(n*5,m*5,5*(100-m**2)**0.5)) for n in range(10) for m in range(10)]
cube = obj3D(batch,win.width,win.height,ptos,ln,0,0,0,vector(0,0,10))
cubeRot = obj3D(batch,win.width,win.height,ptos,ln,0,0,0,vector(1.5,1.5,10))
cube0 = obj3D(batch,win.width,win.height,ptos,ln,0,0,0,vector(0,0,-10))
cube1 = obj3D(batch,win.width,win.height,ptos,ln,0,0,0,vector(50,50,-25))
cube2 = obj3D(batch,win.width,win.height,ptos,ln,0,0,0,vector(40,0,-10))

cam = camera(0,0,0,r=vector(0,45,0),FOV=1000)
cam.rot.abs_rot(-pi/2,0,0)


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
    cubeRot.dnr_dtn[0].x = 4*cos(t)
    cubeRot.dnr_dtn[0].y = 4*sin(t)
    for k in range(10):
        for i in range(4):
            cube_grid[(10*int(t*10) + 10*i + k)%100].rot.rel_rot(0,2*pi*dt/(i+1),0)
            cube_grid[(10*int(t*10) - 10*i + k)%100].rot.rel_rot(0,2*pi*dt/(i+1),0)
    
    cam.rot.rel_rot(Vk_j*dt,Vk_i*dt,Vj_i*dt)
    cam.r += (Vi*cam.rot.i + Vj*cam.rot.j + Vk*cam.rot.k)*dt
pg.clock.schedule_interval(update,1/60)


@win.event
def on_draw():
    win.clear()
    for cubeiter in cube_grid:
        render(cubeiter,cam)
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
        Vk_i = -2
    if symbol==pg.window.key.K:
        Vk_j = -2
    if symbol==pg.window.key.L:
        Vk_i =  2
    if symbol==pg.window.key.U:
        Vj_i = -1
    if symbol==pg.window.key.I:
        Vk_j =  2
    if symbol==pg.window.key.O:
        Vj_i =  1

    if symbol==pg.window.key.A:
        Vi = -10
    if symbol==pg.window.key.S:
        Vk = -10
    if symbol==pg.window.key.D:
        Vi =  10
    if symbol==pg.window.key.R:
        Vj =  10
    if symbol==pg.window.key.W:
        Vk =  10
    if symbol==pg.window.key.F:
        Vj = -10

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