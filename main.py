import Track
import os
from pynput.keyboard import Key, Controller
import multiprocessing
from time import sleep

def BlenderPrg(): 
    os.system('"/Applications/Blender.app/Contents/MacOS/Blender" ./Example.blend')

if __name__ ==  '__main__':
    Obj1T = Track.Tracker("000000")
    keyboard = Controller()
    open('Tracks/Session1/Active.txt', 'w').write('1')

    BlenderProc = multiprocessing.Process(target=BlenderPrg, args=())
    BlenderProc.start()

    print("Start!")
    
    Obj1T.Track()
    
    BlenderProc.join()