# -*-coding: <Utf-8> -*-
from dccpi import *


e = DCCRPiEncoder()
controller = DCCController(e)
def start():
    controller.start()
def stop():
    controller.stop()



class Train:
    def __init__(self, name, adress):
        self.name = name
        self.l = DCCLocomotive(name,adress)
        self.adress = adress
        controller.register(self.l)
        self._speed = 0
            
    def reverse(self):
        """Change the direction"""
        self.l.reverse()  
     
    def stop(self):
        """ Emergency stop. stop controller always"""
        self.l.stop()
        
    def faster():
        """ Increase 1 speed step"""
        self.l.faster()
        
    def slower(self):
        """Reduce the speed"""
        self.l.slower()
        
    def _set_speed(self,new_speed):
        """This function allow us to change the speed"""
        self.l.speed = new_speed
        
    speed = property(_set_speed)
            
    def fl(self,x):
        self.l.fl = x
        
    def f1(self,x):
        self.l.f1 = x
        
    def f2(self,x):
        self.l.f2 = x
        
    def f3(self,x):
        self.l.f3 = x
    
    def f4(self,x):
        self.l.f4 = x
