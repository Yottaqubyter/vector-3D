from stdproyectlib import *
import pyglet as pg
from math import pi,ceil
import jstyleson as json

# POR HACER:
# -[X] Incluir codigo para extraer modelos 3D de archivos json (con `import jstyleson as json`)
# -[ ] Incluir codigo para que haya varios menus (Imagen de fin de partida, menu principal, etc.)
# -[ ] A lo mejor incluir objetos 3D hechos de varios obj3D (para animacion). 
#      Tambien se puede usar una funcion especial para cada animacion que cambie la posicion relativa de los puntos
# -[ ] Hacer un 'R E M A S T E R' del juego corto que use para mostrar las posibilidades del motor 3D obsoleto 

obj_file = open("models.json",'r')
obj_data = json.load(obj_file)
obj_file.close()
for obj_name in obj_data:
    obj_data[obj_name]["points"] = [vector(*i) for i in obj_data[obj_name]["points"]]

win = pg.window.Window(fullscreen=True, resizable=True, caption="vector-3D")
win.set_exclusive_mouse(True)
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

framerate = pg.text.Label('60',x=30,y=30,batch=batch)
grid = obj3D(batch,win.width,win.height,obj_data["Grid"]["points"],obj_data["Grid"]["lines"],0,0,0,vector(0,40,0))
cube_grid = [obj3D(batch,win.width,win.height,obj_data["Piramid"]["points"],obj_data["Piramid"]["lines"],m*0.1,0,0,vector(4*n,4*m,4*(100-m**2)**0.5)) for n in range(10) for m in range(10)]
cube = obj3D(batch,win.width,win.height,obj_data["Cube"]["points"],obj_data["Cube"]["lines"],0,0,0,vector(0,0,0))
cubeRot = obj3D(batch,win.width,win.height,obj_data["Cube"]["points"],obj_data["Cube"]["lines"],0,0,0,vector(0,0,4))
cube0 = obj3D(batch,win.width,win.height,obj_data["Cube"]["points"],obj_data["Cube"]["lines"],0,0,0,vector(0,0,-10))
cube1 = obj3D(batch,win.width,win.height,obj_data["Cube"]["points"],obj_data["Cube"]["lines"],0,0,0,vector(50,50,-25))
cube2 = obj3D(batch,win.width,win.height,obj_data["Cube"]["points"],obj_data["Cube"]["lines"],0,0,0,vector(40,0,-10))

cam = camera(0,0,0,r=vector(0,45,0),FOV=1000)
cam.rot.abs_rot(-pi/2,0,0)


count=0
Vk_j,Vk_i,Vj_i = 0,0,0
Vi,Vj,Vk = 0,0,0
t=0
mouse_x=0
mouse_y=0
mouse_sensibility = 500

def update(dt):
    global count,k_vector,t,mouse_x,mouse_y
    t = t+dt if t<9.9 else 0
    framerate.text = str(int(pg.clock.get_fps()))
    if count<2:
        count+=1
        return None
    cubeRot.dnr_dtn[0].x -= cubeRot.dnr_dtn[0].z*dt # -y*dt
    cubeRot.dnr_dtn[0].z += cubeRot.dnr_dtn[0].x*dt # x*dt
    for k in range(10):
        for i in range(6):
            # cube_grid[(10*t + 10*i + k)%100].dnr_dtn[0] =
            # cube_grid[(10*t - 10*i + k)%100].dnr_dtn[0] =
            cube_grid[(10*int(t*10) + 10*i + k)%100].rot.rel_rot(0,2*pi*dt/(i+1),0)
            cube_grid[(10*int(t*10) - 10*i + k)%100].rot.rel_rot(0,2*pi*dt/(i+1),0)

    cam.rot.abs_rot(0,mouse_x,0)
    cam.r += (Vi*cam.rot.i + Vj*cam.rot.j + Vk*cam.rot.k)*dt
    cam.rot.rel_rot(mouse_y,0,0)
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
    render(grid,cam)
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
''' Para el caso de que sean necesarios de nuevo
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
'''
@win.event
def on_mouse_motion(x,y,dx,dy):
    global mouse_x,mouse_y,mouse_sensibility
    mouse_x += dx/mouse_sensibility
    mouse_y += dy/mouse_sensibility
    mouse_y = min(mouse_y,pi/2)
    mouse_y = max(mouse_y,-pi/2)

pg.app.run()