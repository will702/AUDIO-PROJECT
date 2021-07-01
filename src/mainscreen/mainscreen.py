from kivymd.uix.screen import  MDScreen
from kivy.lang import Builder

import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from os.path import dirname,realpath

folder = dirname(realpath(__file__))


from mainscreen.screen1 import Screen1 
Builder.load_file(folder+"/screen1.kv")
Builder.load_file(folder+"/mainscreen.kv")
class MainScreen(MDScreen):



    def change_screen(self, screen, *args):

        self.ids.screen_manager.current = screen




