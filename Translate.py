import bpy
from time import sleep

object1 = bpy.context.scene.objects["Cube"]

bpy.context.scene.render.filepath = '/Users/jaco/Desktop/Code/TeachP/Tracks/Session1/Out.png'
bpy.context.scene.render.resolution_x = 500
bpy.context.scene.render.resolution_y = 500

while True:
    if open("/Users/jaco/Desktop/Code/TeachP/Tracks/Session1/Active.txt","r").read() == '1':
        Obj0 = open("/Users/jaco/Desktop/Code/TeachP/Tracks/Session1/0.txt","r").read().split(",")
        
        Obj0[0] = int(Obj0[0], 10)
        Obj0[1] = int(Obj0[1], 10)
        Obj0[2] = int(Obj0[2], 10)
        
        object1.location.x = Obj0[0]
        object1.location.y = Obj0[1]
        object1.location.z = Obj0[2]
        
        
        bpy.ops.render.render(write_still=True)
    else:
        break