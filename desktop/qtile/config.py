import os
import subprocess
from libqtile import qtile, bar, layout, widget, hook, backend
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.widget import base

home = os.path.expanduser("~")
mod = "mod4"
alt = "mod1"

mouse_positions: list[tuple[int, int]] = []


# Simple way to debug a message by writing it into ~/debug_qtile.txt
def debug_write(message):
    with open(home + "/debug_qtile.txt", "w") as file:
        file.write(str(message))


def extract_resolution(monitor: bytes) -> tuple[int, int, int, int]:
    loc = monitor.find(b'/') #where the first num ends
    width = int(monitor[:loc])

    loc1 = monitor.find(b'x', loc) + 1 #where the second num starts
    loc2 = monitor.find(b'/', loc1) #where the second num ends
    height = int(monitor[loc1:loc2])

    splitted = monitor[monitor.find(b'+', loc2) + 1:].split(b'+')
    x = int(splitted[0])
    y = int(splitted[1])

    return (width, height, x, y)


def initialize_monitors():
    global monitors
    monitors_raw = subprocess.check_output(['xrandr', '--listmonitors']).splitlines()[1:]
    monitors = list(map(lambda x: extract_resolution(x.split()[2]), monitors_raw)) #grab string resolution and extract ints


def initialize_mouse_positions(monitors: list[tuple[int, int, int, int]]):
    global mouse_positions
    mouse_positions = []
    for monitor in monitors:
        mouse_positions.append((monitor[2] + round(monitor[0] / 2), monitor[3] + round(monitor[1] / 2)))


def get_cur_screen(mouse_pos: tuple[int, int], monitors: list[tuple[int, int, int, int]]) -> int:
    for i in range(len(monitors)):
        monitor = monitors[i]
        if mouse_pos[0] < monitor[2] or mouse_pos[1] < monitor[3]: #mouse not far enough in x nor y
            continue
        elif mouse_pos[0] >= monitor[2] + monitor[0]: #mouse is too far in the x direction
            continue
        elif mouse_pos[1] >= monitor[3] + monitor[1]: #mouse is too far in the y direction
            continue
        else:
            return i #our mouse is within the bounds of the monitor
    return -1 #should be impossible to reach


# Run at Qtile start
@hook.subscribe.startup_once
def autostart():
    global home
    initialize_monitors()
    initialize_mouse_positions(monitors)
    subprocess.run([home + "/autorun.sh"], shell=True)


# On a new client, spawn on the same screen as the mouse initially, otherwise follow the rules 
@hook.subscribe.client_new
def client_new(client: backend.base.Window):

    # have newly opening windows respect the mouse position
    mouse_xpos = qtile.core.get_mouse_position()[0]
    if mouse_xpos <= 1920:  #NOTE: this must be changed for every monitor
        client.cmd_toscreen(0)
    else:
        client.cmd_toscreen(1)

    # move windows to their correct workspace
    classes = client.get_wm_class()
    if 'code-oss' in classes:
        client.togroup('1')
    #if client.name == None: #workaround for spotify, but may affect other programs too
    #    client.togroup('9')
    if 'discord' in classes:
        client.togroup('8')
    
    client.cmd_focus()
    hook.fire("focus_change")


#@hook.subscribe.client_focus
#def win_focus(cur_client):
#    global cur_win
#    cur_win = cur_client


def float_to_front(qtile):
    """
    Bring all floating windows of the group to front
    """
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


# Open the popup calendar 
def open_calendar(qtile):
    subprocess.run([home + "/.config/qtile/popup-calendar.sh --popup"], shell=True)


#Move the mouse to an adjacent screen, move_focus asks if the window focus should follow
def mouse_cycle_screen(qtile):
    global mouse_positions, monitors

    mouse_pos = qtile.core.get_mouse_position()
    cur = get_cur_screen(mouse_pos, monitors)
    if cur + 1 == len(monitors):
        target = 0
    else:
        target = cur + 1
    
    mouse_positions[cur] = mouse_pos
    new_pos = mouse_positions[target]
    subprocess.call(["xdotool", "mousemove", str(new_pos[0]), str(new_pos[1])])
    #if move_focus:
    #    qtile.cmd_next_screen()



#Move the focused window to an adjacent screen, switch_screen asks if the mouse should follow
def window_cycle_screen(qtile, clockwise: bool, switch_screen: bool):
    if len(qtile.screens) < 2:
        return
    cur = qtile.screens.index(qtile.current_screen)

    if clockwise:
        if cur + 1 < len(qtile.screens):
            target = cur + 1 #valid clockwise
        else:
            target = 0 #reset clockwise
    else:
        if cur > 0:
            target = cur - 1 #valid counterclockwise
        else:
            target = len(qtile.screens) - 1 #reset counterclockwise

    group = qtile.screens[target].group.name
    qtile.current_window.togroup(group)
    if switch_screen:
        #mouse_cycle_screen(qtile)
        #debug_write(f"{now_win}, {cur_win}, {qtile.current_window}, {new_win}")
        #qtile.current_window.cmd_focus() #this shit aint working, supposed to focus the moved window
        qtile.cmd_to_screen(target)
        

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod], "i", lazy.function(mouse_cycle_screen), desc="Focus next monitor"),
    Key([mod, "shift"], "i", lazy.function(window_cycle_screen, clockwise=True, switch_screen=True), desc="Follow window to next monitor"),
    Key([mod, "control"], "i", lazy.function(window_cycle_screen, clockwise=True, switch_screen=False), desc="Move window to next monitor"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "space", lazy.spawn("rofi -show run -theme oni"), desc="Run rofi"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "s", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "shift"], "z", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Logout / Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "b", lazy.spawn("nitrogen --restore"), desc="Restart background"),

    Key([mod, alt], "h", lazy.spawn("codium"), desc="Run vscodium"),
    Key([mod, alt], "j", lazy.spawn("firefox"), desc="Run firefox"),
    Key([mod, alt], "k", lazy.spawn("librewolf"), desc="Run librewolf"),
    Key([mod, alt], "l", lazy.spawn("brave"), desc="Run brave"),
    Key([mod, alt], "n", lazy.spawn("thunar"), desc="Run thunar"),
    Key([mod, alt], "m", lazy.spawn("kitty -e lf"), desc="Run lf"),
    Key([mod, alt], "y", lazy.spawn("flatpak run com.mojang.Minecraft"), desc="Run minecraft"),
    Key([mod, alt], "u", lazy.spawn("spotify"), desc="Run spotify"),
    Key([mod, alt], "i", lazy.spawn("discord"), desc="Run discord"),
    Key([mod, alt], "o", lazy.spawn("easyeffects"), desc="Run easyeffects"),

    # Power
    Key([mod], "F1", lazy.spawn("systemctl poweroff"), desc="Shutdown"),
    Key([mod], "F2", lazy.spawn("systemctl reboot"), desc="Restart"),
    Key([mod], "F3", lazy.shutdown(), desc="Logout / Shutdown Qtile"),
    Key([mod], "F4", lazy.spawn("systemctl suspend"), desc="Sleep"),

    Key([mod], "slash", lazy.function(float_to_front), desc="Bring all floating windows forward"),
    Key([mod], "Next", lazy.spawn("redshift -P -O 6500"), desc="Redshift 0"),
    Key([mod], "Prior", lazy.spawn("redshift -P -O 3500"), desc="Redshift 1"),




    

]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group = True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "control"], i.name, lazy.window.togroup(i.name),
                desc="Move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width = 2,
        border_on_single = True,
        insert_position = 1,
        wrap_focus_columns = False,
        wrap_focus_rows = False,
        wrap_focus_stacks = True,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = "sans",
    fontsize = 12,
    padding = 3,
)
defaults = {
    "font": "mono",
    "fontsize": 15,
}

gap = 0

extension_defaults = widget_defaults.copy()


class KeyboardSwitcher(base.InLoopPollText):

    defaults = [
        ("update_interval", 1, "Update time in seconds."),
        (
            "configured_keyboards",
            ["us"],
            "A list of predefined keyboard layouts "
            "represented as strings. For example: "
            "['us', 'us colemak', 'es', 'fr'].",
        ),
        (
            "display_map",
            {},
            "Custom display of layout. Key should be in format "
            "'layout variant'. For example: "
            "{'us': 'us', 'lt sgs': 'sgs', 'ru phonetic': 'ru'}",
        ),
        ("option", None, "string of setxkbmap option. Ex., 'compose:menu,grp_led:scroll'"),
    ]

    def __init__(self, configured_keyboards = ["us"], display_map = dict()):
        widget.TextBox.__init__(self)
        self.add_callbacks(
            {
                "Button1": self.left_click,
                "Button3": self.right_click,
            }
        )
        self.font = defaults['font']
        self.fontsize = defaults['fontsize']
        self.add_defaults(KeyboardSwitcher.defaults)
        self.configured_keyboards = configured_keyboards
        self.display_map = display_map
        self.current = configured_keyboards[0]
        self.index: int = 0
        
    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)

    def poll(self):
        return self.current
    
    def set_keymap(self, keymap: str):
        subprocess.Popen(["setxkbmap", keymap])

    def left_click(self):
        self.index = (self.index + 1) % len(self.configured_keyboards)
        new_keymap = self.configured_keyboards[self.index]
        if new_keymap in self.display_map:
            self.current = self.display_map[new_keymap]
        else:
            self.current = new_keymap
        self.set_keymap(new_keymap)
        self.tick()

    def right_click(self):
        self.index = (self.index - 1) % len(self.configured_keyboards)
        new_keymap = self.configured_keyboards[self.index]
        if new_keymap in self.display_map:
            self.current = self.display_map[new_keymap]
        else:
            self.current = new_keymap
        self.set_keymap(new_keymap)
        self.tick()


screens = [
    Screen(
        top=bar.Gap(gap),
        left=bar.Gap(gap),
        right=bar.Gap(gap),
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    
                    highlight_method = "line",
                    highlight_color = ["#464646FF", "#464646FF"], #gradient
                   
                    block_highlight_text_color = None, #font color for focused workspaces 
                    active = "#FFFFFF",     #font color for workspaces with windows
                    inactive = "#767676",   #font color for workspaces without windows, always affects this focused tab when other screen focused
                    
                    this_current_screen_border = "#FF5555",     #highlight current screen when current screen in focus
                    other_screen_border = "#77DDDD",            #highlight other screen when current screen in focus
                    
                    this_screen_border = "#FF5555",             #highlight this screen when other screens in focus
                    other_current_screen_border = "#77DDDD",    #highlight other screens when other screens in focus
                    
                    disable_drag = True, #disable dragging workspaces around
                    borderwidth = 4, #border of weird things, but affects tag width and highlight height
                ),
                widget.Prompt(),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CPU(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.GenPollText(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    update_interval=1,
                    func=lambda: subprocess.getoutput("ip addr | grep inet | grep enp37s0 | awk '{print $2}'")
                ),
                widget.Spacer(),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.CurrentLayout(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                KeyboardSwitcher(
                    configured_keyboards = ['us', 'es', 'semimak-jq', 'mtgap', 'colemak-dh'],
                    display_map = { #makes everything lowercase
                        'us': 'us',
                        'es': 'es',
                        'workman': 'wm',
                        'semimak-jq': 'sm',
                        'mtgap': 'mt',
                        'colemak-dh': 'cm',
                    }
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.Systray(),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.Clock(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    format="%m/%d/%Y %a %I:%M %p",
                    mouse_callbacks = {
                        'Button1': lazy.function(open_calendar),
                    }
                ),
            ],
            25,
            background = "#00000000",
            margin = [gap, 0, 0, 0],
        ),
    ),
    Screen(
        top=bar.Gap(gap),
        left=bar.Gap(gap),
        right=bar.Gap(gap),
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    
                    highlight_method = "line",
                    highlight_color = ["#464646FF", "#464646FF"], #gradient
                   
                    block_highlight_text_color = None, #font color for focused workspaces 
                    active = "#FFFFFF",     #font color for workspaces with windows
                    inactive = "#767676",   #font color for workspaces without windows, always affects this focused tab when other screen focused
                    
                    this_current_screen_border = "#77DDDD",     #highlight current screen when current screen in focus
                    other_screen_border = "#FF5555",            #highlight other screen when current screen in focus
                    
                    this_screen_border = "#77DDDD",             #highlight this screen when other screens in focus
                    other_current_screen_border = "#FF5555",    #highlight other screens when other screens in focus
                    
                    disable_drag = True, #disable dragging workspaces around
                    borderwidth = 4, #border of weird things, but affects tag width and highlight height
                ),
                widget.Prompt(),
                widget.Spacer(),
                widget.CurrentLayout(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.Clock(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    format="%m/%d/%Y %a %I:%M %p",
                    mouse_callbacks = {
                        'Button1': lazy.function(open_calendar),
                    }
                ),
            ],
            25,
            background = "#00000000",
            margin = [gap, 0, 0, 0],
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Tor Browser"),  # Needs a fixed window size to avoid fingerprinting by screen size
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"

