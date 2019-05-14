import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.uix.stacklayout import StackLayout
from random import shuffle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import time
from kivy.uix.carousel import Carousel



Window.clearcolor = 1, 1, 1, 1
# Window.size = 360, 640

seconds = 20

global current_seconds
global default_time

class RootWidget(FloatLayout):
    def AddPlayer(self):
        if(self.ids.player_name_input.text != ""):
            #print("Player Added")
            self.ids.player_list.add_widget(Bt(text=str(self.ids.player_name_input.text)), index=0)
            self.ids.player_name_input.text = ""
                # print(PlayerList().self.index)
    pass


default_time = 300

class Options(FloatLayout):
    def White(self, i):
        self.children[i].background_color = [.7, .9, .4, 1]

    def Green(self, i):
        self.children[i].background_color = [1, 1, 1, 1]


class Timer(Button):
    def StartTime(self):
        current_seconds = default_time + 1
        current_seconds -= 1
        minutes = current_seconds // 60
        if (minutes < 10 and current_seconds % 60 < 10):
            for_time = "0" + str(minutes) + ":" + "0" + str(current_seconds % 60)
        elif (minutes < 10 and current_seconds % 60 >= 10):
            for_time = "0" + str(minutes) + ":" + str(current_seconds % 60)
        elif (minutes >= 10 and current_seconds % 60 < 10):
            for_time = str(minutes) + ":" + "0" + str(current_seconds % 60)
        else:
            for_time = str(minutes) + ":" + str(current_seconds % 60)
        return for_time

    def NewTimeWindow(self):
        self.parent.add_widget(TimerInput())
        #print("Window open")
        self.parent.widget_disabled = True
    pass
            # return for_time


current_seconds = default_time


class Functions(BoxLayout):
    # def CurrentTime(self):
    #     current_seconds = default_time + 1
    #     return current_seconds
    def White(self, i):
        self.children[i].background_color = [.7, .9, .4, 1]

    def Green(self, i):
        self.children[i].background_color = [1, 1, 1, 1]

    start_beep = SoundLoader.load('beep1.ogg')
    end_beep = SoundLoader.load('beep2.ogg')

    def NewPlayerWindow(self):
        self.parent.add_widget(PlayerInput())
        #print("Window open")
        self.parent.widget_disabled = True

    def TimerOn(self):
        if self.ids.start.text == "PLAY":
            self.ids.start.text = "STOP"
            self.ids.start.color = 1, 0, 0, 1
            self.ClockRunning()
        else:
            self.ids.start.text = "PLAY"
            self.ids.start.color = 1, 1, 1, 1
            self.ClockStop()


    def ClockRunning(self):
        if current_seconds > 0:
            #global current_seconds
            self.start_beep.play()
            # current_seconds -= 1
            return Clock.schedule_interval(self.RunTime, 1)
        else:
            return self.ClockStop()

    def ClockStop(self):
        Clock.unschedule(self.RunTime)

    def RunTime(self, dt):
        global current_seconds
        current_seconds -= 1
        self.UpdateLabel(for_time=self.FormatTime())

        if(current_seconds == 0):
            self.end_beep.play()
            self.StopClock()

    def FormatTime(self):
        minutes = current_seconds // 60
        if (minutes < 10 and current_seconds % 60 < 10):
            for_time = "0" + str(minutes) + ":" + "0" + str(current_seconds % 60)
        elif (minutes < 10 and current_seconds % 60 >= 10):
            for_time = "0" + str(minutes) + ":" + str(current_seconds % 60)
        elif (minutes >= 10 and current_seconds % 60 < 10):
            for_time = str(minutes) + ":" + "0" + str(current_seconds % 60)
        else:
            for_time = str(minutes) + ":" + str(current_seconds % 60)
        return for_time

    def UpdateLabel(self, for_time):
        self.parent.parent.ids.clock.text = for_time
        #print(self.parent.parent.ids.clock.text)

    def StopClock(self):
        self.ids.start.text = "PLAY"
        self.ids.start.color = 1, 1, 1, 1
        self.ClockRunning()
        player_list_index = self.parent.parent.ids.player_list.children

        del_text = player_list_index[len(player_list_index) - 1].children[0].children[0].text
        player_list_index[len(player_list_index) - 1].Del()
        self.parent.parent.ids.player_list.add_widget(widget=BtReady(text=del_text), index=len(player_list_index))

        #print("Done!")
    # def ResetTimer(self):
            # player_list_index[len(player_list_index) - 1].bind.on_press = Bt().RemovePlayer()
        # return current_seconds


rootwidget = RootWidget()


class PlayerList(BoxLayout):
    pass


class Randomize(FloatLayout):
    sound = SoundLoader.load('shuffle.ogg')

    def Randomize(self):
        self.sound.play()
        #print(self.parent.parent.parent.ids.player_list.children)
        shuffle(self.parent.parent.parent.ids.player_list.children)
        #print(self.parent.parent.parent.ids.player_list.children)

    def White(self):
        self.children[0].background_color = [.7, .9, .4, 1]

    def Green(self):
        self.children[0].background_color = [1, 1, 1, 1]

class PlayerInput(FloatLayout):
    def RemoveWindow(self):
        self.parent.remove_widget(self)

    def AddPlayer(self):
        if self.ids.player_name_input.text != "":
            #print("Player Added")
            # self.parent.parent.ids.player_list.add_widget(Bt(text=str(self.ids.player_name_input.text)), index=0)
            text = str(self.ids.player_name_input.text)
            self.parent.parent.ids.player_list.add_widget(PlayerCarousel(), index=0)
            self.parent.parent.ids.player_list.children[0].add_widget(Bt(text=text), index=1)
            self.RemoveWindow()

    # def CheckEnter(self):
    #     if RootWidget().ids.player_name_input.keyboard_on_key_down(keycode="enter") == True:
    #         print("oi")

    # def _on_keyboard_down(self, keycode):
    #     if keycode[1] == 'enter':
    #         print("oi")


class TimerInput(FloatLayout):
    def NewTime(self):
        if (self.ids.timer_seconds_input.text != ""):
            global current_seconds
            global default_time
            default_time = int(self.ids.timer_seconds_input.text)
            current_seconds = int(self.ids.timer_seconds_input.text)
            self.parent.parent.ids.func.UpdateLabel(for_time=self.parent.parent.ids.func.FormatTime())
            self.RemoveWindow()
            return current_seconds

    def RemoveWindow(self):
        self.parent.remove_widget(self)


class Bt(Button):
    def RemovePlayer(self):
        if len(self.parent.parent.parent.ids.player_list.children) > 1:
            global current_seconds
            #print(len(self.parent.children) - 1)
            self.parent.parent.parent.ids.clock.text = self.parent.parent.parent.ids.clock.StartTime()
            current_seconds = default_time
            self.parent.parent.parent.ids.func.TimerOn()
            self.Del()
            return current_seconds
        else:
            self.Del()
    def TextSize(self):
        textsize = self.parent.parent.parent.parent.height
        return textsize

    def Del(self):
        self.parent.remove_widget(self)



class PlayerCarousel(Carousel):
    def Del(self):
        self.parent.remove_widget(self)
    def Text(self):
        text = self.text
        return text
    # def TextLabel(self):
    #     text =
    #     return text



    pass


class BtReady(Bt):
    pass


class BtDelete(Bt):
    def Del(self):
        self.parent.parent.Del()
    pass


class PlayerBox(DragBehavior, BoxLayout):
    pass


class SoccerSwapApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    SoccerSwapApp().run()

