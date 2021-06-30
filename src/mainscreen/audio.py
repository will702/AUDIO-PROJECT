from kivy.utils import platform
class Player(object):
    if platform == 'android':
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
            self.mPlayer.setAudioStreamType(self.AudioManager.STREAM_MUSIC)
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


player = Player()
