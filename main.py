
from kivy.core.window import Window
# Window.borderless = False
import kivy
kivy.require("1.11.1")

from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.utils import platform

import time, threading

if platform == 'android':
    import jnius
    from jnius import autoclass
KV = """
<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)
    
RootLay:
    ScreenManager:
        id: _screen_manager
        Screen:
            name:'home'
            MDToolbar:
                pos_hint: {'top': 1, 'right': 1}
                title: "Thread Test"
            MDLabel:
                id: is_thread
                text: 'Stopped'
                pos_hint: {"center_x": .8, "center_y": .8}
                height: 50
                halign: "center"
                markup: True
            MDRectangleFlatIconButton:
                text: "Run Thread"
                icon: 'lan-disconnect'
                pos_hint: {"center_x": .5, "center_y": .6}
                on_release:
                    root.start_thread()
            MDCheckbox:
                id: check_id
                on_active: root.on_checkbox_active(*args)
                active: False
                size_hint: None, None
                size: "48dp", "48dp"
                pos_hint: {'center_x': .8, 'center_y': .4}
            MDRectangleFlatIconButton:
                id: second
                text: "Test"
                icon: 'bluetooth-connect'
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release:
                    if root.ids.check_id.active and root.ids.switch_id.active: print("Both active")
                    elif root.ids.check_id.active: print("Checkbox active")
                    elif root.ids.switch_id.active: print("Switch active")
                    elif root.ids.red.active or root.ids.green.active: print("Radio active")
                    else: print('None active')
            MDSwitch:
                id: switch_id
                on_active: root.on_switch_active(*args)
                pos_hint: {'center_x': .2, 'center_y': .4}
                width: dp(64)
            Check:
                id: red
                active: True
                pos_hint: {'center_x': .4, 'center_y': .4}
        
            Check:
                id: green
                pos_hint: {'center_x': .6, 'center_y': .4}
            MDLabel:
                id: message
                text: 'Not Received'
                pos_hint: {"center_x": .5, "center_y": .3}
                height: 50
                halign: "center"
                markup: True
"""

class RootLay(FloatLayout):

    def __init__(self, **kwargs):
        super(RootLay, self).__init__(**kwargs)
        self._running = False
        self._check = False
        self.t = None
        self.t1 = None

    def terminate(self):
        self._running = False

    def runit(self, n):
        while self._running and n > 0:
            self.ids.is_thread.text = 'Running..'
            print('Counting seconds', n)
            s = (5 - n) / 5 * 100
            self.ids.message.text = str(s) + '%'
            n -= 1
            time.sleep(1)
        s = (5 - n) / 5 * 100
        self.ids.message.text = str(s) + '%'
        self.terminate()
        self._check = False
        if self.t1 is not None:
            if self.t1.is_alive():
                print('is alive')
        print('not alive')
        self.t1 = None
        self.ids.is_thread.text = 'Stopped'
    def run_check(self, n):
        while self._check and n > 0:
            if self.t1 is not None:
                if self.t1.is_alive():
                    print(' t1 is alive')
                else:
                    print(' t1 is dead')
            time.sleep(1)
        self._check = False
        if self.t is not None:
            if self.t.is_alive():
                print('is alive')
        print('not alive')
        self.t = None

    def start_thread_one(self):
        self._check = True
        if self.t is None:
            self.t = threading.Thread(target=self.run_check, args=(5,))
            self.t.start()

    def start_thread(self):
        self._running = True
        if self.t1 is None:
            self.t1 = threading.Thread(target=self.runit, args=(5,))
            self.ids.is_thread.text = 'Starting..'
            self.t1.start()
        self.start_thread_one()
    def on_checkbox_active(self, checkbox, value):
        if value:
            print(value, ' ', checkbox.active, 'The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
        else:
            print(value, ' ', checkbox.active, 'The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
    def on_switch_active(self, switch, value):
        if value:
            print(value, ' ', switch.active, 'The switch', switch, 'is active', 'and', switch.state, 'state')
        else:
            print(value, ' ', switch.active, 'The switch', switch, 'is inactive', 'and', switch.state, 'state')

class MainApp(MDApp):
    def build(self):
        self.title = "Thread Test"
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.primary_hue = "400"
        self.use_kivy_settings = False
        return Builder.load_string(KV)

    def on_pause(self):
        return True

    def on_stop(self):
        return True

    def on_resume(self):
        return True

MainApp().run()