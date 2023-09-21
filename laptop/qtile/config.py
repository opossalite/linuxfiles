import os
import subprocess

from libqtile import qtile, bar, layout, widget, hook, backend
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.command import lazy
from libqtile.utils import send_notification
from libqtile.widget import base


home = os.path.expanduser('~')
mod = "mod4"
alt = "mod1"

mouse_positions: list[tuple[int, int]] = []
monitors: list[tuple[int, int, int, int]] = []


def debug_write(message):
    """Writes into ~/.debug_qtile.txt"""
    with open(home + "/debug_qtile.txt", "w") as file:
        file.write(str(message))
       

def debug_notif(message):
    """Shows a notification via dunst"""
    message = str(message).replace("<", '').replace(">", '')
    subprocess.run([f"dunstify --timeout=2000 debug \"{message}\"" ], shell=True)


def extract_resolution(monitor: bytes) -> tuple[int, int, int, int]:
    """I think this converts one monitor's string into a resolution and position"""
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
    """Retrieves monitor resolutions and positions"""
    global monitors
    monitors_raw = subprocess.check_output(['xrandr', '--listmonitors']).splitlines()[1:]
    monitors = list(map(lambda x: extract_resolution(x.split()[2]), monitors_raw)) #grab string resolution and extract ints


def initialize_mouse_positions(monitors: list[tuple[int, int, int, int]]):
    """Initializes mouse position for each screen"""
    global mouse_positions
    mouse_positions = []
    for monitor in monitors:
        mouse_positions.append((monitor[2] + round(monitor[0] / 2), monitor[3] + round(monitor[1] / 2)))


def get_cur_screen(mouse_pos: tuple[int, int], monitors: list[tuple[int, int, int, int]]) -> int:
    """Get the current screen the mouse is on"""
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


@hook.subscribe.startup_once
def autostart():
    """Run at Qtile start"""
    global home 
    initialize_monitors()
    initialize_mouse_positions(monitors)
    subprocess.run([home + "/autorun.sh"], shell=True)

    
@hook.subscribe.startup
def startup():
    """Runs any time Qtile is restarted"""
    initialize_monitors()
    initialize_mouse_positions(monitors)


@hook.subscribe.client_new
def client_new(client: backend.base.Window):
    """Runs when a client is spawned, moves clients to their correct workspaces"""
    classes = client.get_wm_class()

    if 'code' in classes:
        client.togroup('1')
    elif 'discord' in classes:
        client.togroup('8')
    #if client.name == None: #workaround for spotify, but affects other programs too
    #    client.togroup('9')
    else: #no assigned window, so spawn on current screen
        mouse_pos = qtile.core.get_mouse_position()
        cur = get_cur_screen(mouse_pos, monitors)
        client.cmd_toscreen(cur)

    client.cmd_focus()
    hook.fire("focus_change")


@hook.subscribe.screen_change
def screens_reconfigured(event):
    """Runs when screen configuration is changed"""
    initialize_monitors()
    initialize_mouse_positions(monitors)



def float_to_front(qtile):
    """Bring all floating windows of the group to front"""
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


def swap_workspaces(qtile, target):
    """Swap all windows in the current and target workspaces"""
    cur_group = qtile.current_group
    cur_windows = qtile.current_group.windows.copy()
    target_group = [x for x in qtile.groups if x.name == target.name][0]
    target_windows = target_group.windows.copy()
    for cur_win in cur_windows:
        cur_win.togroup(target_group.name)
    for target_win in target_windows:
        target_win.togroup(cur_group.name)


def all_to_workspace(qtile, target):
    """Move all current windows to the target workspace"""
    cur_windows = qtile.current_group.windows.copy()
    for cur_win in cur_windows:
        cur_win.togroup(target.name)


# Open the popup calendar 
def open_calendar(qtile):
    subprocess.run([home + "/.config/qtile/popup-calendar.sh --popup"], shell=True)
   

#Move the mouse to an adjacent screen, move_focus asks if the window focus should follow
def mouse_cycle_screen(qtile, clockwise: bool):
    """Move the mouse to the next or previous screen"""
    global mouse_positions, monitors

    if len(qtile.screens) < 2:
        return

    mouse_pos = qtile.core.get_mouse_position()
    cur = get_cur_screen(mouse_pos, monitors)

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

    mouse_positions[cur] = mouse_pos
    new_pos = mouse_positions[target]
    subprocess.call(["xdotool", "mousemove", str(new_pos[0]), str(new_pos[1])])
    qtile.cmd_to_screen(target)



def window_cycle_screen(qtile, clockwise: bool, switch_screen: bool):
    """Move focused window to next or previous screen, also asks if mouse should follow"""
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
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #Key([mod], "i", lazy.next_screen(), desc='Focus next monitor'),
    Key([mod], "i", lazy.function(mouse_cycle_screen, clockwise = True), desc="Focus next monitor"),
    Key([mod, "shift"], "i", lazy.function(window_cycle_screen, clockwise = True, switch_screen = True), desc="Follow window to next monitor"),
    Key([mod, "control"], "i", lazy.function(window_cycle_screen, clockwise = True, switch_screen = False), desc="Move window to next monitor"),
    #Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "s", lazy.window.toggle_floating(), desc="Toggle floating"),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod], "o", lazy.spawn("gsimplecal"), desc="Run gsimplecal"),

    # Open programs
    #Key([mod, alt], "Semicolon", lazy.spawn("code"), desc="Run code"),
    #Key([mod, alt], "p", lazy.spawn("steam"), desc="Run steam"),
    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "space", lazy.spawn("rofi -show run -theme cobalt"), desc="Run dmenu"),

    Key([mod, alt], "h", lazy.spawn("code"), desc="Run code"),
    Key([mod, alt], "j", lazy.spawn("firefox"), desc="Run firefox"),
    Key([mod, alt], "k", lazy.spawn("librewolf"), desc="Run librewolf"),
    Key([mod, alt], "l", lazy.spawn("brave"), desc="Run brave"),
    Key([mod, alt], "n", lazy.spawn("thunar"), desc="Run thunar"),
    Key([mod, alt], "m", lazy.spawn("kitty -e lf"), desc="Run lf"),
    Key([mod, alt], "y", lazy.spawn("flatpak run com.mojang.Minecraft"), desc="Run minecraft"),
    Key([mod, alt], "u", lazy.spawn("spotify"), desc="Run spotify"),
    Key([mod, alt], "i", lazy.spawn("discord"), desc="Run discord"),
    Key([mod, alt], "o", lazy.spawn("easyeffects"), desc="Run easyeffects"),
    
    # Restart Applications
    Key([mod, "shift"], "b", lazy.spawn("nitrogen --restore"), desc="Restart background"),
    #Key([mod, "shift"], "p", lazy.spawn("./.config/polybar/launch.sh"), desc="Restart polybar"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),

    # Lighting
    Key([mod], "KP_Up", lazy.spawn("brightnessctl set 10%+"), desc="Brightness up"),
    Key([mod, "shift"], "KP_Up", lazy.spawn("brightnessctl set 1%+"), desc="Brightness slight up"),
    Key([mod], "KP_Down", lazy.spawn("brightnessctl set 10%-"), desc="Brightness down"),
    Key([mod, "shift"], "KP_Down", lazy.spawn("brightnessctl set 1%-"), desc="Brightness slight down"),
    Key([mod, "control"], "KP_Down", lazy.spawn("redshift -P -O 6500"), desc="Redshift 0"),
    Key([mod, "control"], "KP_Up", lazy.spawn("redshift -P -O 3500"), desc="Redshift 1"),
    Key([mod, "control"], "KP_Left", lazy.spawn("redshift -P -O 2500"), desc="Redshift 2"),
    Key([mod, "control"], "KP_Right", lazy.spawn("redshift -P -O 1500"), desc="Redshift 3"),
    Key([mod], "Next", lazy.spawn("redshift -P -O 6500"), desc="Redshift 0"),
    Key([mod], "Prior", lazy.spawn("redshift -P -O 3500"), desc="Redshift 1"),

    #Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -M set Master 5%+"), desc="Volume up"),
    #Key(["shift"], "XF86AudioRaiseVolume", lazy.spawn("amixer -M set Master 1%+"), desc="Volume slight up"),
    #Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -M set Master 5%-"), desc="Volume down"),
    #Key(["shift"], "XF86AudioLowerVolume", lazy.spawn("amixer -M set Master 1%-"), desc="Volume slight down"),
    #Key([], "XF86AudioMute", lazy.spawn("amixer -M set Master toggle"), desc="Volume toggle mute"),

    # Power
    Key([mod], "F1", lazy.spawn("systemctl poweroff"), desc="Shutdown"),
    Key([mod], "F2", lazy.spawn("systemctl reboot"), desc="Restart"),
    Key([mod], "F3", lazy.shutdown(), desc="Logout / Shutdown Qtile"),
    Key([mod], "F4", lazy.spawn("systemctl suspend"), desc="Sleep"),


    # Close window
    Key([mod, "shift"], "z", lazy.window.kill(), desc="Kill focused window"),

    #Spawn prompt
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    # Miscellaneous
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    #xdotool key U00D1
    #xdotool key shift+U00D1
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc="Switch to & move focused window to group {}".format(i.name)),
            # Or, use below if you prefer not to switch to that group.
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "control"], i.name, lazy.window.togroup(i.name), desc="Move focused window to group {}".format(i.name)),

            Key([mod, "shift", "control"], i.name, lazy.function(swap_workspaces, target = i), desc="Swaps two workspaces"),
            Key([mod, "mod1", "control"], i.name, lazy.function(all_to_workspace, target = i), desc=f"Moves all current windows to workspace {i.name}"),

        ]
    )

layouts = [
    layout.Columns(
        #border_focus_stack=["#d75f5f", "#8f3d3d"],
        #border_focused = "#881111",
        #border_focus = "#5294e2",
        #border_focus = "#2222BB",
        #border_focus = "#5fafff",
        border_focus = "#2254e2",
        border_normal = "#000022",
        border_width = 2,
        border_on_single = True,
        
        insert_position = 1, #insert after the current window
        wrap_focus_columns = False,
        wrap_focus_rows = False,
        wrap_focus_stacks = True,
        ), 
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

defaults = {
    'font': "mono",
    'fontsize': 15,
}


class KeyboardSwitcher(base.InLoopPollText):

    def __init__(self, configured_keyboards: list[tuple[str, str]] = [("us", "us")]):
        widget.TextBox.__init__(self)
        self.add_callbacks(
            {
                "Button1": self.left_click,
                "Button3": self.right_click,
            }
        )
        self.font = defaults['font']
        self.fontsize = defaults['fontsize']
        #self.add_defaults(KeyboardSwitcher.defaults)
        #self.display_map = display_map
        #self.configured_keyboards = list(map(lambda x: x[0], configured_keyboards))
        self.configured_keyboards = configured_keyboards
        self.index: int = 0
        
    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)

    def poll(self):
        return self.configured_keyboards[self.index][1]
    
    def set_keymap(self):
        global home
        keymap = self.configured_keyboards[self.index][0]
        #to turn the current layout into a config, run this: xkbcomp -xkb $DISPLAY xkbmap
        #subprocess.Popen(["setxkbmap", keymap])
        file_loc = home + "/.keymaps/" + keymap + ".xkb"
        subprocess.Popen(["xkbcomp", "-w", "0", file_loc, ":0"])  #apparently $DISPLAY is :0

    def left_click(self):
        self.index = (self.index + 1) % len(self.configured_keyboards)
        self.set_keymap()
        self.tick()

    def right_click(self):
        self.index = (self.index - 1) % len(self.configured_keyboards)
        self.set_keymap()
        self.tick()


screens = [
    Screen(
        bottom=bar.Bar(
            [
                #widget.CurrentScreen(
                #    font = "mono",
                #    fontsize = 15,
                #    
                #    active_text = "A",
                #    active_color = "#00FF00",
                #    inactive_text = "I",
                #    inactive_color = "#FF0000",
                #    #active_text = " ● ACTIVE ●", #"●",
                #    #active_color = "#FF5555",
                #    #inactive_text = " ○ ACTIVE ○", #"○",
                #    #inactive_color = "#767676",
                #),
                widget.GroupBox(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'] + 2,
                    
                    highlight_method = "line",
                    highlight_color = ["#464646FF", "#464646FF"], #gradient
                   
                    block_highlight_text_color = None, #font color for focused workspaces 
                    active = "#FFFFFF",     #font color for workspaces with windows
                    inactive = "#767676",   #font color for workspaces without windows, always affects this focused tab when other screen focused
                    
                    #this_current_screen_border = "#5fafff",     #highlight current screen when current screen in focus
                    this_current_screen_border = "#2288ff",     #highlight current screen when current screen in focus
                    other_screen_border = "#77DDDD",            #highlight other screen when current screen in focus
                    
                    this_screen_border = "#FF5555",             #highlight this screen when other screens in focus
                    other_current_screen_border = "#77DDDD",    #highlight other screens when other screens in focus
                    
                    disable_drag = True, #disable dragging workspaces around
                    borderwidth = 4, #border of weird things, but affects tag width and highlight height
                ),
                widget.Prompt(),
                #widget.WindowName(),
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
                widget.Memory(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    format = ' Memory {MemUsed:.1f}{mm}/{MemTotal:.1f}{mm}', #the .1f means one digit after the dot
                    measure_mem = 'G',
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
                #widget.Sep(
                #    linewidth = 0,
                #    padding = 6,
                #),
                widget.Spacer(),
                widget.CurrentLayout(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                #widget.Net(interface="enp37s0"),
                #widget.GenPollText(update_interval=1, func=lambda: subprocess.check_output("sh /path/to/foo.sh").decode("utf-8")),
                #widget.KeyboardLayout(
                #    font = defaults['font'],
                #    fontsize = defaults['fontsize'],
                #    configured_keyboards = ['us', 'es'],
                #    display_map = {
                #        'us': 'us',
                #        'es': 'es',
                #    }
                #),
                KeyboardSwitcher(
                    configured_keyboards = [
                        ("us", "us"),
                        ("es", "es"),
                        ("colemak-dha", "cm"),
                        #("colemak-dh", "cm"),
                        ("semimak-jq", "sm"),
                        ("mtgap", "mt"),
                    ]

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
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.Clock(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    format="%m/%d/%Y %a %I:%M %p",
                    mouse_callbacks = {
                        'Button1': lazy.spawn("gsimplecal"),
                    }
                ),
                #widget.QuickExit(),
            ],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            #border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            #background = "#282A2EFF",
            background = "#2A2A2AFF",
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    fontsize = 15,
                    
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
                #widget.WindowName(),
                widget.Spacer(),
                widget.CurrentLayout(),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Clock(
                    format="%m/%d/%Y %a %I:%M %p",
                    mouse_callbacks = {
                        'Button1': lazy.spawn("gsimplecal"),
                    }
                ),
                #widget.QuickExit(),
            ],
            25,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background = "#00000000",
        ),
    ),
    #Screen(
    #    bottom=bar.Bar(
    #        [
    #            widget.CurrentLayout(),
    #            widget.CurrentScreen(font="mono"),
    #            widget.GroupBox(),
    #            widget.Prompt(),
    #            widget.WindowName(),
    #            #widget.Chord(
    #            #    chords_colors={
    #            #        "launch": ("#ff0000", "#ffffff"),
    #            #    },
    #            #    name_transform=lambda name: name.upper(),
    #            #),
    #            #widget.TextBox("default config", name="default"),
    #            #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
    #            widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
    #        ],
    #        25,
    #        # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
    #        # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
    #    ),
    #),
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
bring_front_click = False
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
        Match(title="Tor Browser"),  # Needs a fixed window size to avoid fingerprinting by screen size.
    ],
    #border_focus = "#881111",
    border_focus = "#5294e2",
    #border_default = "#220000",
    border_default = "#000022",
    border_width = 1,
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

