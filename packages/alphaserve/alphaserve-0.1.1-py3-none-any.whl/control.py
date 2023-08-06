import os
import platform
from pynput import mouse, keyboard
from pynput.keyboard import KeyCode # used for creating own media keys, as default ones currently do not work with x11

m = mouse.Controller()
k = keyboard.Controller()

mediaKeysLinux = {
    'vol_mute':269025042,
    'vol_down':269025041,
    'vol_up':269025043
}

class Mouse():
    currDelta = (0,0)
    def __init__(self):
        pass
        
    def resetDelta(self):
        self.currDelta = (0,0)

    def move(self, movX, movY, velocityX=1.0, velocityY=1.0):
        currPos = m.position
        
        deltaX = (abs(movX) * velocityX - self.currDelta[0])
        deltaY = (abs(movY) * velocityY - self.currDelta[1])
        
        #currPos = (currPos[0]+deltaX, currPos[1]+deltaY)
        
        # pynput uses relative movement
        m.move(deltaX, deltaY)
        #input()
        return
    
    def tap(self, button=1):
        #posX, posY = m.position()
        #m.click(posX, posY, button)
        m.click(mouse.Button.left)
        
    def scroll(self, deltaY):
        scroll_units = 1
        if deltaY < 0:
            scroll_units = -1
        m.scroll(scroll_units)

class Keyboard():
    switcher = {
            "f5": keyboard.Key.f5 ,
            "f11": keyboard.Key.f11 ,
            "up": keyboard.Key.up ,
            "down": keyboard.Key.down ,
            "left": keyboard.Key.left ,
            "right": keyboard.Key.right ,
            "space": keyboard.Key.space ,
            }
    def __init__(self):
        pass
   
    def vol(self, val):
        if val > 0:
            try:
                k.tap(keyboard.Key.media_volume_up)
            except:
                k.tap(KeyCode(mediaKeysLinux["vol_up"]))
        elif val < 0:
            try:
                k.tap(keyboard.Key.media_volume_down)
            except:
                k.tap(KeyCode(mediaKeysLinux["vol_down"]))
        elif val == 0:
            try:
                k.tap(keyboard.Key.media_volume_mute)
            except:
                k.tap(KeyCode(mediaKeysLinux["vol_mute"]))

    def tap_key(self, key):
        if len(key) > 1:
            int_key = self.switcher.get(key.lower(), -1)
            if int_key == -1:
                raise Exception("key is not implemented: " + str(key))
            k.tap(int_key)
        else:
            k.tap(key)

class Control():
    def __init__(self):
        pass

    
    def shutdown(self, mode_time_tuple):
        system = platform.system()
        if system == "Windows":
            try:
                os.system("shutdown /s")
            except Exception as e:
                print(e)
            return
        if system == "Linux":
            try:
                os.system("shutdown -t 10")
            except Exception as e:
                print(e)
            pass
