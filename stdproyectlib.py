from math import cos, sin
import pyglet as pg

def opsum(l):
    k = l[0]
    for i in l[1:]:
        k += i
    return k

def istype(l, tp):
    for i in l:
        if type(i)!=tp:
            return False
    return True


class vector:

    def __init__(self,x,y,z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "vector("+str(self.x)+","+str(self.y)+","+str(self.z)+")"

    def __str__(self):
        return str(self.x)+"*(i)" + " + " + str(self.y)+"*(j)" + " + " + str(self.z)+"*(k)"

    def __eq__(self,other):
        if type(self)!=type(other):
            return False
        else:
            return (self.x==other.x and self.y==other.y and self.z==other.z)

    def __add__(self, other):
        return vector(self.x+other.x,self.y+other.y,self.z+other.z)
    def __sub__(self, other):
        return vector(self.x-other.x,self.y-other.y,self.z-other.z)
    def __mul__(self, other):
        if type(other) is vector:
            return self.x*other.x + self.y*other.y + self.z*other.z # Producto escalar
        else:
            return vector(self.x*other,self.y*other,self.z*other)
    def __matmul__(self, other):
        return vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
    def __truediv__(self, other):
        return self*(1/other)
    def __floordiv__(self, other):
        if type(other)==vector:
            return NotImplemented
        else:
            return vector(self.x//other,self.y//other,self.z//other)
    def __mod__(self, other):
        return NotImplemented # Podria hacerse, pero inutil
    def __divmod__(self, other):
        return NotImplemented
    def __pow__(self, other):
        return NotImplemented
    def __lshift__(self, other):
        return NotImplemented
    def __rshift__(self, other):
        return NotImplemented
    def __and__(self, other):
        return NotImplemented
    def __xor__(self, other):
        return NotImplemented
    def __or__(self, other):
        return NotImplemented

    def __radd__(self, other): # other+self
        return vector(self.x+other.x,self.y+other.y,self.z+other.z)
    def __rsub__(self, other): # other-self
        return vector(other.x-self.x,other.y-self.y,other.z-self.z)
    def __rmul__(self, other): # other*self
        if type(other)==vector: # Producto escalar
            return self.x*other.x + self.y*other.y + self.z*other.z
        else:
            return vector(self.x*other,self.y*other,self.z*other)
    def __rmatmul__(self, other):
        return -(self@other)
    def __rtruediv__(self, other):
        # other/self(vecto) !!! No se puede dividir entre un vector
        return NotImplemented
    def __rfloordiv__(self, other):
        return NotImplemented
    def __rmod__(self, other):
        return NotImplemented
    def __rdivmod__(self, other):
        return NotImplemented
    def __rpow__(self, other):
        return NotImplemented
    def __rlshift__(self, other):
        return NotImplemented
    def __rrshift__(self, other):
        return NotImplemented
    def __rand__(self, other):
        return NotImplemented
    def __rxor__(self, other):
        return NotImplemented
    def __ror__(self, other):
        return NotImplemented

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    def __imul__(self, other):
        if type(other)==vector:
            return NotImplemented
            # No añadir el producto escalar aquí
            # crearía confusion por el cambio de tipos.
        else:
            self.x *= other
            self.y *= other
            self.z *= other
            return self
    def __imatmul__(self, other):
        return NotImplemented
    def __itruediv__(self, other):
        self *= 1/other
        return self
    def __ifloordiv__(self, other):
        if type(other)==vector:
            return NotImplemented
        else:
            self.x //= other
            self.y //= other
            self.z //= other
            return self
    def __imod__(self, other):
        return NotImplemented
    def __ipow__(self, other):
        return NotImplemented
    def __ilshift__(self, other):
        return NotImplemented
    def __irshift__(self, other):
        return NotImplemented
    def __iand__(self, other):
        return NotImplemented
    def __ixor__(self, other):
        return NotImplemented
    def __ior__(self, other):
        return NotImplemented

    def __neg__(self):
        return vector(-self.x,-self.y,-self.z)
    def __pos__(self):
        return vector(+self.x,+self.y,+self.z)
    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def __int__(self):
        return vector(int(self.x),int(self.y),int(self.z))
    def __float__(self):
        return vector(float(self.x),float(self.y),float(self.z))

# Algunos vectores estandar
null_vector = vector(0,0,0)
i_vector = vector(1,0,0)
j_vector = vector(0,1,0)
k_vector = vector(0,0,1)

class UTransform: 
    """
    Contiene informacion sobre los 3 vectores unitarios
    se usa para especificar direccion
    """
    def __init__(self,i=i_vector,j=j_vector,k=k_vector):
        if i*j!=0 or i*k!=0 or j*k!=0:
            raise TypeError("Los vectores de orientacion, si se especifican, deben de ser perpendiculares entre sí")
        self.i, self.j, self.k = i/abs(i), j/abs(j), k/abs(k)
    
    def abs_rot(self,k_j,k_i,j_i):
        """
        Especifica una serie de angulos fijar la orientacion de la camara
        """
        global i_vector, j_vector, k_vector
        i = +i_vector
        j = +j_vector
        k = +k_vector
        k = cos(k_j)*k + sin(k_j)*j     # Posicion de los vectores en espacio 3D:
        j = k@i                         # 
        k = cos(k_i)*k + sin(k_i)*i     #    j k    y z
        i = j@k                         #    |/     |/
        j = cos(j_i)*j + sin(j_i)*i     #   -·-i   -·-x
        i = j@k                         #   /|     /|
        self.i = i                      #
        self.j = j                      #
        self.k = k                      #

    def rel_rot(self,k_j,k_i,j_i):
        """
        Especifica una serie de angulos para rotar la camara
        """
        self.k = cos(k_j)*self.k + sin(k_j)*self.j     # Posicion de los vectores en espacio 3D:
        self.j = self.k@self.i                         # 
        self.k = cos(k_i)*self.k + sin(k_i)*self.i     #     j k     y z
        self.i = self.j@self.k                         #     |/      |/
        self.j = cos(j_i)*self.j + sin(j_i)*self.i     #    -·-i    -·-x
        self.i = self.j@self.k                         #    /|      /|
        self.k /= abs(self.k)                          #
        self.i /= abs(self.i)                          #
        self.j /= abs(self.j)                          #


class camera:
    """Camera object. Consists of 4 vectors, indicating position and orientation in 3d spcace"""

    def __init__(self, k_j, k_i, j_i, FOV=1, r=null_vector):
        global i_vector,j_vector,k_vector
        self.rot = UTransform(i_vector,j_vector,k_vector)
        self.rot.abs_rot(k_j,k_i,j_i)
        self.r = r
        self.FOV = FOV


class body:
    def __init__(self, r0, *args):
        if not istype((r0,)+args , vector):
            raise TypeError("Expected vector type arguments: body(vector, vector, ...)")
        self.dnr_dtn = [r0]+list(args) # [r, dr/dt, d**2r/dt**2, d**3r/dt**3]
        self.events = {"on_update":(lambda k:None)}

    def update(self,dt):
        self.events["on_update"](dt)
        for i in range(self.get_n()-1):
            self.dnr_dtn[i] += self.get_dnr_dtn(i+1)*dt

    def get_n(self):
        return len(self.dnr_dtn)

    def get_dnr_dtn(self,n):
        return self.dnr_dtn[n]

    def set_dnr_dtn(self, n, val):
        self.dnr_dtn[n] = val
    
    def event(self, func):
        """
        Se usa para definir eventos
        """
        self.events[func.__name__] = func
        return func


def PRend(v,c):
    """
    Calcula la posicion de un punto en el cuadro a partir de un objeto camara y el factor FOV
    """
    return c.FOV*vector( ((v - c.r)*c.rot.i)/((v - c.r)*c.rot.k) , ((v - c.r)*c.rot.j)/((v - c.r)*c.rot.k) )

def render(obj,c):
    """
    Dibuja el objeto 3d en el lugar adecuado tras calcular su aspecto una vez realizada la proyeccion conica
    """
    obj.__render__(c)

def rendbool(v,c):
    """
    Le dice al programa si el vector se debe calcular en pantalla o no. 
    Util para evitar que objetos detras de la camara o lejanos se muestren.
    """
    return (v - c.r)*c.rot.k>0.05 # Incluir otros filtros


class obj3D(body):
    """
    Un objeto en el espacio 3D
    """
    def __init__(self, batch, width, height, ptos, ln, k_j, k_i, j_i, r, *args, color=(255,255,255)):
        global i_vector,j_vector,k_vector
        super().__init__(r, *args)
        self.events["on_render"] = lambda c:None
        self.rot = UTransform(i_vector,j_vector,k_vector)
        self.rot.abs_rot(k_j,k_i,j_i)
        if istype(ptos,vector):
            self.ptos = ptos
        else:
            raise TypeError("Expected vector list as ptos")
        self.ln = [ [pg.shapes.Line(0,0,0,0, batch = batch, color = color), i] for i in ln]
        self._w = width/2
        self._h = height/2
    
    def __render__(self, c):
        """
        Se calcula el aspecto una vez realizada la proyeccion conica del objeto
        Para dibujarlo, solo tienes que usar la batch que has usado como parametro antes
        """
        ptos2D = []
        args = [None, c]
        for p in self.ptos:
            args[0] = self.dnr_dtn[0] + self.rot.i*p.x + self.rot.j*p.y + self.rot.k*p.z
            if rendbool(*args):
                ptos2D += [PRend(*args)]
            else:
                ptos2D += [None]
    
        render_event = False
        for l,i in self.ln:
            if ptos2D[i[0]]!=None and  ptos2D[i[1]]!=None:
                render_event = True
                l.x  = self._w + ptos2D[i[0]].x
                l.y  = self._h + ptos2D[i[0]].y
                l.x2 = self._w + ptos2D[i[1]].x
                l.y2 = self._h + ptos2D[i[1]].y
            l.visible = ptos2D[i[0]]!=None and  ptos2D[i[1]]!=None
        if render_event: self.events["on_render"](c)
    
    def set_color(self, color):
        for l,_ in self.ln:
            l.color = color
