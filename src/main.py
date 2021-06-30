# coding: utf8
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from jnius import autoclass

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from kivy.core.window import Window
from kivy.factory import Factory
from src import MainScreen

if platform == 'android':
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

if platform == 'macosx':
    Window.size = (450,750)


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.kivy.oscservice',
    servicename=u'Pong'
)



class ClientServerApp(MDApp):
    a = 0

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.service = None
        # self.start_service()
        self.data =   {

                "Pause":"pause",
                "Play Again":"play",
                "Loop":"repeat",
                }
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
    def call(self,button):
        if button.icon == 'play':
            self.play_again()
        if button.icon == 'pause':
            self.pause()
        if button.icon == 'repeat':
            self.set_loop()


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
                # print(self.asw)
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
    def set_loop(self):
        self.client.send_message(b'/loop_again', [])

    def play_again(self):
        self.client.send_message(b'/play_again',[])
    def pause(self):
        self.client.send_message(b'/pause',[])
    def send(self, *args, argumen):
        print(argumen)
        self.client.send_message(b'/ping', [f'{argumen}'.encode('utf-8')])


if __name__ == '__main__':
    ClientServerApp().run()