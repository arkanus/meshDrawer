"""
    This example show how to use MeshDrawer to draw
    on the screen in any way shape or form you want
"""
import direct.directbase.DirectStart
from pandac.PandaModules import *
from random import *
from math import *

maxParticles = 500 # max number of particle (1000) triangles we will display
by = 16 # we have a 16x16 plate texture

generator = MeshDrawer()
generator.setBudget(maxParticles)
## this line is no longer required; in fact it causes an error :]
#generator.setPlateSize(by)
generatorNode = generator.getRoot()
generatorNode.reparentTo(render)
generatorNode.setDepthWrite(False)
generatorNode.setTransparency(True)
generatorNode.setTwoSided(True)
generatorNode.setTexture(loader.loadTexture("radarplate.png"))
generatorNode.setBin("fixed",0)
generatorNode.setLightOff(True)

# load some thing into our scene
base.setFrameRateMeter(True)
base.setBackgroundColor(.1,.1,.1,1)
t = loader.loadModel('teapot')
t.reparentTo(render)
t.setPos(0,0,-1)

# very usefull function
def randVec():
    return Vec3(random()-.5,random()-.5,random()-.5)


def Frame(framenum):
    """
    This function returns the Vec4 with the values for u, v, width and height as
    expected by the lastest Meshdrawer implementation instead of setting up a
    plate.
    """
    w = h = 2048.0
    frame_w = frame_h = 128.0

    factor_x = factor_y = 1.0 / float(w / frame_w)

    x_max = int(w / float(frame_w))
    y_max = int(h / float(frame_h))

    y = int((framenum - 1) / x_max )
    x = int(framenum - (y * x_max) - 1)

    u = float(x*factor_x)
    v = float(1 - ((y+1) * factor_y))

    ue = factor_x
    ve = factor_y

    return Vec4(u, v, ue, ve)

seed(1988)  # random seed - remove if you always want different random results

# create 100 random particles
particles = []
for i in range(100):
    frame = Frame(randint(181, 207))
    p = [randVec()*1, randVec()*100, frame, 1, Vec4(random(),random(),random(),1)]
    particles.append(p)

# create 100 random lines
lines = []
for i in range(100):
    l = [randVec()*100,randVec()*100, Frame(194),.1,Vec4(random(),random(),random(),1)]
    lines.append(l)

def drawtask(taks):
    """ this is called every frame to regen the mesh """
    t = globalClock.getFrameTime()
    generator.begin(base.cam,render)
    for v,pos,frame,size,color in particles:
        generator.billboard(pos+v*t,
                            frame,
                            size*sin(t*2)+3,
                            color)

    for start,stop,frame,size,color in lines:
        generator.segment(start,
                          stop,
                          frame,
                          size*sin(t*2)+2,
                          color)
    generator.end()
    return taks.cont

# add the draw task to be drawn every frame
taskMgr.add(drawtask, "draw task")

# run the sample
run()

