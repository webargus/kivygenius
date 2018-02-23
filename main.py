import kivy
kivy.require('1.1.3')

from kivy.core.audio import SoundLoader
from random import randint
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class GeniusSounds:
    sounds = [SoundLoader.load('sound_0.wav'), SoundLoader.load('sound_1.wav'), SoundLoader.load('sound_2.wav'),
              SoundLoader.load('sound_3.wav'), SoundLoader.load('error.mp3')]

    def __init__(self):
        for sound in self.sounds:
            sound.seek(0)
            sound.volume = 1

class GeniusSequence:

    def __init__(self):
        self.sequence = []
        self.ix = 0

    def seed(self):
        self.sequence.append(randint(0, 3))

    def clear(self):
        del self.sequence[:]
        self.ix = 0

    def reset(self):
        self.ix = 0

    def is_last_seed(self):
        return self.ix == len(self.sequence)

    def next(self):
        if self.is_last_seed():
            return
        self.ix += 1

    def get(self):
        if self.is_last_seed():
            return -1
        return self.sequence[self.ix]

    def match(self, seed):
        if self.is_last_seed():
            return False
        return self.sequence[self.ix] == int(seed)

class GeniusGridLayout(GridLayout):

    def __init__(self, **kwargs):
        super(GeniusGridLayout, self).__init__(**kwargs)
        self.seq = GeniusSequence()
        self.isRepeating = False

    def btnReleased(self, btn_id):

        # discard player clicks when game repeating sequence
        if self.isRepeating:
            return;

        print("btn_id=", btn_id)
        # advance sequence index to next button id if player got it right; add a new id if
        # player reached the end of the sequence; end game if user got it wrong
        if self.seq.match(btn_id):
            GeniusSounds.sounds[int(btn_id)].play()
            self.seq.next()
            if self.seq.is_last_seed():
                Clock.schedule_once(self.appendTouch, 2)
        else:
            GeniusSounds.sounds[-1].play()
            print("Game Over!")

    def startGame(self):
        self.seq.clear()

        # add first color button challenge to player
        self.appendTouch()

    # append another button press to the sequence and replay the whole sequence for the player
    def appendTouch(self, *dt):

        # generate new button random id between 0 and 3 and add it to the sequence
        self.seq.seed()

        # replay the sequence for the user
        self.seq.reset()
        self.isRepeating = True
        Clock.schedule_interval(self.replaySequence, .5)

    def replaySequence(self, *dt):
        if self.seq.is_last_seed():    # no more seeds
            Clock.unschedule(self.replaySequence)
            # point sequence index back to first button
            self.seq.reset()
            # enable player clicks
            self.isRepeating = False
        else:
            # get btn obj by id
            btn_id = self.seq.get()
            btn = self.ids['btn_' + str(btn_id)]
            # toggle btn
            if btn.state == 'normal':
                GeniusSounds.sounds[btn_id].play()
                btn.state = 'down'
            else:
                btn.state = 'normal'
                self.seq.next()

class Genius(App):

    def build(self):
        return GeniusGridLayout()

    def on_pause(self):
        return True

if __name__ == '__main__':
    Genius().run()





