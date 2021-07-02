from kivy.core.audio import SoundLoader
class Player:
    loader = None
    def load(self,content):
        if self.loader != None:
            try:
                self.loader.stop()
                self.loader.reset()
            except:
                pass
        self.loader =SoundLoader.load(content)

    def play(self):




        self.loader.play()

    def end(self):
        self.loader.stop()
        self.loader.reset()
player = Player()



