# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from typing import List

from libqtile import qtile, bar, layout, widget, hook, backend
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.command import lazy
from xcffib.xproto import EventMask

from pynput.mouse import Button, Controller

home = os.path.expanduser('~')
mouse_pynput = Controller()
mouse_positions = []

# Run at Qtile start
@hook.subscribe.startup_once
def autostart():
    global mouse_positions
    subprocess.run([home + "/autorun.sh"], shell=True)
    
  
# Focus newly spawned windows, not working currently 
@hook.subscribe.client_managed
def client_new(client):
    client.cmd_focus()
    hook.fire("focus_change") 
    

# MARKED FOR UPDATING, refactor this code
# On a new client, spawn on the same screen as the mouse initially, otherwise follow the rules 
@hook.subscribe.client_new
def client_new(client: backend.base.Window):
    #backend.x11.window.Window
    #backend.base.Window
    #with open(home + "/temp.txt", 'w') as file:
    #    file.write(client.name + str(client.get_wm_role()) + str(client.get_wm_type()))
    #with open(home + "/temp.txt", 'w') as file:
    #    file.write(qtile.core.get)

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


# MARKED FOR DEPRECATION
def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)
            mouse_to_next_screen(qtile)
    else:
        window_to_next_screen(qtile, switch_group, switch_screen)


# MARKED FOR UPDATING: absorb above function and also implement wrapping
def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if len(qtile.screens) < 2:
        return
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1) #will need to remove the cmd_ in the future
            mouse_to_next_screen(qtile)
    else:
        window_to_previous_screen(qtile, switch_group, switch_screen)
        

# Focus the next screen and bring mouse with it 
def mouse_to_next_screen(qtile, move_focus = False):
    global mouse_positions, mouse_pynput
    
    if len(mouse_positions) == 0: #initialize mouse_positions if necessary
        initialize_mouse_positions(qtile)
        
    mouse_pos = qtile.core.get_mouse_position()
    screen_index = determine_monitor(qtile, mouse_pos) #determine the current monitor
    
    mouse_positions[screen_index] = mouse_pos #save the current mouse position before switching
    
    #switch focus and mouse position
    mouse_pynput.position = mouse_positions[(screen_index + 1) % len(qtile.screens)]
    if move_focus == True:
        qtile.cmd_next_screen() #will need to remove the cmd_ in the future


# Initialize mouse positions    
def initialize_mouse_positions(qtile):
    global mouse_positions
    mouse_positions = [0]*len(qtile.screens) #set the right size
    screen_offset = 0   #consider the size of each screen
    for i, screen in enumerate(qtile.screens): #iterate through all screens
        mouse_positions[i] = (screen.width / 2 + screen_offset, screen.height / 2) #set the initial place to the center of each monitor
        screen_offset += screen.width
    

# Simple way to debug a message by writing it into ~/debug_qtile.txt
def debug_write(message):
    with open(home + "/debug_qtile.txt", "w") as file:
        file.write(str(message))
       

# Open the popup calendar 
def open_calendar(qtile):
    subprocess.run([home + "/.config/qtile/popup-calendar.sh --popup"], shell=True)
   

# Given a set of coordinates, determine which monitor we're on 
def determine_monitor(qtile, coords):
    screen_index = 0
    screen_offset = 0 #considers each monitor's width

    for screen in qtile.screens:
        if coords[0] > screen.width + screen_offset:
            screen_index += 1
            screen_offset += screen.width
        else:
            break
        
    return screen_index
    

mod = "mod4"
alt = "mod1"
terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #Key([mod], "i", lazy.next_screen(), desc='Focus next monitor'),
    Key([mod], "i", lazy.function(mouse_to_next_screen, move_focus = True), desc="Focus next monitor"),
    Key([mod, "shift"], "i", lazy.function(window_to_next_screen, switch_screen = True), desc="Follow window to next monitor"),
    Key([mod, "control"], "i", lazy.function(window_to_next_screen), desc="Move window to next monitor"),
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

    # Open programs
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "space", lazy.spawn("dmenu_run -nb '#282828' -sf '#FF5555' -sb '#464646' -nf '#bbbbbb'"), desc="Run dmenu"),
    Key([mod, alt], "n", lazy.spawn("nemo"), desc="Run nemo"),
    Key([mod, alt], "f", lazy.spawn("firefox"), desc="Run firefox"),
    Key([mod, alt], "b", lazy.spawn("brave"), desc="Run brave"),
    Key([mod, alt], "l", lazy.spawn("librewolf"), desc="Run librewolf"),
    Key([mod, alt], "v", lazy.spawn("code"), desc="Run code"),
    Key([mod, alt], "d", lazy.spawn("discord"), desc="Run discord"),
    Key([mod, alt], "m", lazy.spawn("alacritty --command lf"), desc="Run lf"),
    Key([mod, alt], "s", lazy.spawn("spotify"), desc="Run spotify"),
    Key([mod, alt], "t", lazy.spawn("steam"), desc="Run steam"),
    
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
                lazy.window.togroup(i.name, switch_group=True),
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
        #border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_focused = "#881111",
        border_normal = "#220000",
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
    # layout.Bsp(),
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
    'fontsize': 14,
}

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
                widget.Systray(),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                widget.KeyboardLayout(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    configured_keyboards = ['us', 'es'],
                    display_map = {
                        'us': 'us',
                        'es': 'es',
                    }
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
                #widget.QuickExit(),
            ],
            25,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background = "#00000000",
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
                        'Button1': lazy.function(open_calendar),
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
    border_focus = "#881111",
    border_default = "#220000",
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

