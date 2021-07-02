'p4a example service using oscpy to communicate with main application.'
import os
os.environ['KIVY_AUDIO'] = 'android'

from kivy.utils import platform
from mainscreen.audio import player
from time import  sleep
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient


class Service(object):

    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    CLIENT = OSCClient('localhost', 3002)
    a = 0





    def __init__(self):

        self.SERVER.bind(b'/ping', self.ping)
        self.SERVER.bind(b'/pause',self.pause)
        self.SERVER.bind(b'/play_again',self.play_again)
        self.SERVER.bind(b'/loop_again', self.loop_again)


        while True:
            pass






    def loop_again(self):
        self.a+=1


        #
        # if platform != 'android':
        #     if self.a%2 !=0:
        #
        #         pemutar.do_loop(True)
        #     else:
        #         pemutar.do_loop(False)

        if self.a % 2 != 0:

            player.loader.loop = True
        else:
            player.loader.loop = False

    def play_again(self):
        # if platform != 'android':
        #     pemutar.resume()
        if platform == 'android':
            player.loader.play()

    def pause(self):

        if platform == 'android':
            player.loader.stop()

    def ping(self,*_):
        'answer to ping messages'
        filename = _[0].decode('utf-8')

        self.filename = filename
        self.send_date()

































    def run_music(self):



        if platform == 'android':

            player.load(self.filename)


            self.CLIENT.send_message(
                b'/message',
                [
                    f'{self.filename}'.encode('utf-8'),
                ], )




    def send_date(self):





        self.run_music()





                

if __name__ == '__main__':
    service = Service()



