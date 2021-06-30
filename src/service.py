'p4a example service using oscpy to communicate with main application.'

from time import  sleep
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from kivy.utils import platform
class MediaPlayer(object):
    from jnius import autoclass

    MediaPlayer = autoclass('android.media.MediaPlayer')
    AudioManager = autoclass('android.media.AudioManager')
    mPlayer = MediaPlayer()

    def raw(self):
        return self.mPlayer

    def play(self, content):
        self.content = str(content)
        try:
            self.mPlayer.stop()
            self.mPlayer.reset()
        except:
            pass
        self.mPlayer.setDataSource(self.content)
        self.mPlayer.prepare()
        self.mPlayer.start()

    def pause(self):
        self.mPlayer.pause()

    def resume(self):
        self.mPlayer.start()

    def stop(self):
        self.mPlayer.stop()

    def stream(self, content):
        self.content = str(content)
        self.mPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC)
        try:
            self.mPlayer.stop()
            self.mPlayer.reset()
        except:
            pass
        self.mPlayer.setDataSource(self.content)
        self.mPlayer.prepare()
        self.mPlayer.start()

    def get_duration(self):
        if self.content:
            return self.mPlayer.getDuration()

    def current_position(self):
        if self.content:
            return self.mPlayer.getCurrentPosition()

    def seek(self, value):
        try:
            self.mPlayer.seekTo(int(value) * 1000)
        except:
            pass

    def do_loop(self, loop=False):
        if not loop:
            self.mPlayer.setLooping(False)
        else:
            self.mPlayer.setLooping(True)

    def is_playing(self):
        return self.mPlayer.isPlaying


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
                from jnius import autoclass

                MediaPlayer = autoclass('android.media.MediaPlayer')
                AudioManager = autoclass('android.media.AudioManager')
                mPlayer = MediaPlayer()
                mPlayer.setDataSource(self.filename)

                mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
                mPlayer.prepare()

                mPlayer.start()
                sleep(mPlayer.getDuration())
                mPlayer.stop()




    def send_date(self):

        'send date to the application'




        self.run_music()




                

if __name__ == '__main__':
    service = Service()



