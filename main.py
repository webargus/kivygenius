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


class GeniusGridLayout(GridLayout):

    sequence = []
    isRepeating = False
    ix = 0

    def btnReleased(self, btn_id):

        # discard player clicks when game repeating sequence
        if self.isRepeating:
            return;

        print("btn_id=", btn_id)
        # advance sequence index to next button id if player got it right; add a new id if
        # player reached the end of the sequence; end game if user got it wrong
        if (len(self.sequence) > 0) and (self.sequence[self.ix] == int(btn_id)):
            GeniusSounds.sounds[int(btn_id)].play()
            self.ix = self.ix + 1
            if self.ix == len(self.sequence):
                try:
                    Clock.schedule_once(self.appendTouch, 2)
                except Exception as e:
                    print(e)
        else:
            GeniusSounds.sounds[-1].play()
            print("Game Over!")
            self.isPlaying = False


    def startGame(self):
        # create sequence list if it wasn't created yet; don't know how to create it
        # in constructor __init__ without messing with game grid layout
        del self.sequence[:]

        # add first color button challenge to player
        self.appendTouch()

    # append another button press to the sequence and replay the whole sequence for the player
    def appendTouch(self, *dt):

        # generate new button random id between 0 and 3 and add it to the sequence
        self.sequence.append(randint(0, 3))

        # replay the sequence for the user
        self.ix = 0
        self.isRepeating = True
        Clock.schedule_interval(self.setBtnState, .5)

    def setBtnState(self, *dt):
        if self.ix == len(self.sequence):
            # end sequence replay and await player clicks
            Clock.unschedule(self.setBtnState)
            # point sequence index back to first button
            self.ix = 0
            # enable player clicks
            self.isRepeating = False
        else:
            # get current button id in the sequence
            btn_id = str(self.sequence[self.ix])
            # get btn obj by id
            btn = self.ids['btn_'+btn_id]
            # toggle btn
            if btn.state == 'normal':
                GeniusSounds.sounds[int(btn_id)].play()
                btn.state = 'down'
            else:
                btn.state = 'normal'
                # point index to next button id in sequence
                self.ix = self.ix + 1

class Genius(App):

    def build(self):
        return GeniusGridLayout()

    def on_pause(self):
        return True

if __name__ == '__main__':
    Genius().run()





