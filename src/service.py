'p4a example service using oscpy to communicate with main application.'

from time import  sleep
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from kivy.utils import platform
from mainscreen.audio import player

class Service(object):
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)

    CLIENT = OSCClient('localhost', 3002)
    if platform == 'android':

        filename = ''
    else:
        filename = ''


    def __init__(self):

        self.SERVER.bind(b'/ping', self.ping)
        while True:
            sleep(1)



    
    def ping(self,*_):
        'answer to ping messages'
        filename = _[0].decode('utf-8')
        self.filename = filename
        self.send_date()
    def run_music(self):
        if platform == 'macosx':
            if self.filename != '':
                from kivy.core.audio import SoundLoader
                SoundLoader.load(self.filename).play()

        if platform == 'android':
            if self.filename != '':
                player.play(self.filename)

                # from jnius import autoclass
                #
                # MediaPlayer = autoclass('android.media.MediaPlayer')
                # AudioManager = autoclass('android.media.AudioManager')
                # mPlayer = MediaPlayer()
                # mPlayer.setDataSource(self.filename)
                #
                # mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
                # mPlayer.prepare()
                #
                # mPlayer.start()
                # sleep(mPlayer.getDuration())
                # mPlayer.stop()




    def send_date(self):





        self.run_music()




                

if __name__ == '__main__':
    service = Service()



