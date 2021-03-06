# coding: utf8
import os
from os import environ
#IF THERE IS ANDROID_BOOTLOGO IN DICT NAME ENVIRON SO IT WILL BE ANDROID
if 'ANDROID_BOOTLOGO' in environ:
    os.environ['KIVY_AUDIO'] = 'android'
else:
    #IF NOT IT IS NOT ANDROID
    print("!Android")

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty

from mainscreen.audio import player


from mainscreen.mainscreen import MainScreen



if platform == 'android':
    from android.permissions import request_permissions, Permission




    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
from jnius import autoclass



if platform == 'macosx':
    Window.size = (450,750)


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)

from kivymd.uix.slider import MDSlider

class MySlider(MDSlider):
    sound = ObjectProperty(None)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            # call super method and save its return
            ret_val = super(MySlider, self).on_touch_up(touch)

            # adjust position of sound
            self.sound.seek(self.max * self.value_normalized)

            # if sound is stopped, restart it
            if self.sound.state == 'stop':
                MDApp.get_running_app().start_play()

            # return the saved return value
            return ret_val
        else:
            return super(MySlider, self).on_touch_up(touch)

class ClientServerApp(MDApp):
    a = 0
    b = 0
    pilihan = 0
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.service = None
        # self.start_service()

        self.server = server = OSCThreadServer()
        server.listen(
            address=b'localhost',
            port=3002,
            default=True,
        )


        self.client = OSCClient(b'localhost', 3000)
        self.screen = Builder.load_file('main.kv')
        self.start_service()
        self.asw = ''

        return self.screen


    def choose_next(self):
        try:
            if platform == 'android':
                from random import choice
                from glob import glob
                dir = glob('/sdcard/*.wav')
                selected = choice(dir)
            else:
                from random import choice
                from glob import glob
                dir = glob('*.wav')
                selected =choice(dir)
            try:
                self.screen.ids.mainscreen.ids.screen1.ids.container.remove_widget(self.slider)
            except AttributeError:
                pass

            try:

                player.load(selected)

                self.slider = MySlider(min=0, max=player.loader.length, value=0, sound=player.loader,
                                       pos_hint={'center_x': 0.50, 'center_y': 0.6},
                                       size_hint=(0.6, 0.1))

                self.screen.ids.mainscreen.ids.screen1.ids.container.add_widget(self.slider)

                self.updater = None
                self.start_play()


            except AttributeError:

                print(player.loader.length)
        except:
            pass




    def recent(self):
        try:
            try:
                self.screen.ids.mainscreen.ids.screen1.ids.container.remove_widget(self.slider)
            except AttributeError:
                pass









            try:


                player.load(player.filename)
                self.slider = MySlider(min=0, max=player.loader.length, value=0, sound=player.loader,
                                       pos_hint={'center_x': 0.50, 'center_y': 0.6},
                                       size_hint=(0.6, 0.1))

                self.screen.ids.mainscreen.ids.screen1.ids.container.add_widget(self.slider)

                self.updater = None
                self.start_play()


            except AttributeError:

                print(player.loader.length)
        except:
            pass
    def selected(self, filename, asw, budi):
        for i in range(1):
            #Making For I in range to use continue

            if self.a == 0:
                self.asw = asw[0]

                self.popup = Factory.CustomPopup()

                self.popup.text = asw[0]

                self.popup.open()
                self.a = 1
                #so if self.a == 0 so self .a will be 1 and if 1 it will be executed again so i used continue

                continue




            if self.a == 1 :

                if self.asw == asw[0]:
                    self.popup = Factory.CustomPopup()

                    self.popup.text = asw[0]

                    self.popup.open()


                if self.asw != asw[0]:
                    self.asw = asw[0]



                    self.popup = Factory.CustomPopup()

                    self.popup.text = asw[0]

                    self.popup.open()



    def start_service(self):
        if platform == 'android':
            service = autoclass(SERVICE_NAME)
            self.mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(self.mActivity, argument)
            self.service = service

        elif platform in ('linux', 'linux2', 'macosx', 'win'):
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['service.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()
        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )

    def stop_service(self):
        if self.service:
            if platform == "android":
                self.service.stop(self.mActivity)
            elif platform in ('linux', 'linux2', 'macos', 'win'):
                # The below method will not work.
                # Need to develop a method like
                # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s03.html
                self.service.stop()
            else:
                raise NotImplementedError(
                    "service start not implemented on this platform"
                )
            self.service = None
    def send(self,argumen):
        self.display_message(argumen)

    def set_loop(self):
        self.b+=1
        from kivymd.toast import toast
        if self.b % 2 != 0:

            player.loader.loop = True
            toast("Loop Set To True")
        else:
            player.loader.loop = False
            toast("Loop Set To False")


    def play_again(self):

        player.play()
        player.loader.seek(self.last)


    def pause(self):

        player.loader.stop()
        self.last = player.loader.get_pos()

    def start_play(self, *args):
        # play the sound
        from kivy.clock import Clock
        player.loader.play()

        if self.updater is None:
            # schedule updates to the slider
            self.updater = Clock.schedule_interval(self.update_slider, 0.5)

    def update_slider(self, dt):
        # update slider
        try:
            self.slider.value = player.loader.get_pos()

            # if the sound has finished, stop the updating
            if player.loader.state == 'stop':
                self.updater.cancel()
                self.updater = None
        except:
            pass

    def display_message(self, message):

        try:
            self.screen.ids.mainscreen.ids.screen1.ids.container.remove_widget(self.slider)
        except AttributeError:
            pass









        try:


            player.load(message)
            self.slider = MySlider(min=0, max=player.loader.length, value=0, sound=player.loader,
                                   pos_hint={'center_x': 0.50, 'center_y': 0.6},
                                   size_hint=(0.6, 0.1))

            self.screen.ids.mainscreen.ids.screen1.ids.container.add_widget(self.slider)

            self.updater = None
            self.start_play()


        except AttributeError:

            print(player.loader.length)




if __name__ == '__main__':
    ClientServerApp().run()