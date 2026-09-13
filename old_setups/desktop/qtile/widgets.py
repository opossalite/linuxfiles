import os
import subprocess
from libqtile import widget
from libqtile.widget import base


home = os.path.expanduser("~")


class KeyboardSwitcher(base.InLoopPollText):

    def __init__(self, configured_keyboards: list[tuple[str, str]] = [("us", "us")]):
        global home
        widget.TextBox.__init__(self)
        self.add_callbacks(
            {
                "Button1": self.left_click,
                "Button3": self.right_click,
            }
        )
        self.configured_keyboards = configured_keyboards
        self.index: int = 0
        self.keymap_location = home + "/.keymaps/"
        
    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)

    def poll(self):
        return self.configured_keyboards[self.index][1]
    
    def set_keymap(self):
        global home
        keymap = self.configured_keyboards[self.index][0]
        file_loc = self.keymap_location + keymap + ".xkb"
        subprocess.Popen(["xkbcomp", "-w", "0", file_loc, ":0"])  #apparently $DISPLAY is :0

    def left_click(self):
        self.index = (self.index + 1) % len(self.configured_keyboards)
        self.set_keymap()
        self.tick()

    def right_click(self):
        self.index = (self.index - 1) % len(self.configured_keyboards)
        self.set_keymap()
        self.tick()



