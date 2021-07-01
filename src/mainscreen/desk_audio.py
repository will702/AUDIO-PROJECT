from kivy.core.audio import SoundLoader
class Player(object):





    def play(self, content):
        self.content = str(content)
        try:
            self.sound = None
        except:
            pass
        self.sound = SoundLoader.load(self.content)

        self.sound.play()
    def pause(self):
        self.sound.stop()

    def resume(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()


    def get_duration(self):
        if self.content:
            return self.sound.length


    def current_position(self):
        if self.content:
            return self.sound.get_pos()

    def seek(self, value):
        try:
            self.sound.seek(value)
        except:
            pass

    def do_loop(self, loop=False):
        if not loop:
            self.sound.loop = False
        else:
            self.sound.loop = True

    def is_playing(self):
        return self.sound.state
pemutar  = Player()
