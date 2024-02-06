import os
import subprocess
import socket

from libqtile import qtile, bar, layout, widget, hook, backend
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.command import lazy
from libqtile.widget import base


hostname = socket.gethostname()
home = os.path.expanduser('~')
mod = "mod4"
alt = "mod1"

mouse_positions: list[tuple[int, int]] = []
monitors: list[tuple[int, int, int, int]] = []


match hostname:
    case "VulpesKrovPC":
        border_focus = "#881111"
        border_normal = "#220000"
        this_screen_tag = "#FF5555"
        other_screen_tag = "#77DDDD"
        bar_height = 25
        bar_background = "#00000000"
        floating_border_focus = "#0000FF"
        floating_border_default = "#000022"
        rofi_theme = "oni"
        strict_workspaces = True #only enforce strict workspaces, any not listed are dynamic
        strict_map = [
            { #two monitors
                8: 1, #workspace: screen
                9: 1,
                0: 1,
            },
            { #three monitors
                8: 1,
                9: 1,
                0: 1,
            },
        ]
    case "CobaltCanidPC":
        border_focus = "#2254e2"
        border_normal = "#000022"
        this_screen_tag = "#2288ff"
        other_screen_tag = "#AF87FF"
        bar_height = 30
        bar_background = "#2A2A2AFF"
        floating_border_focus = "#5294e2"
        floating_border_default = "#000022"
        rofi_theme = "cobalt"
        strict_workspaces = False #only enforce strict workspaces, any not listed are dynamic
        strict_map = [
            { #two monitors
                8: 0, #workspace: screen
                9: 0,
            },
            { #three monitors
                8: 0,
                9: 0,
            },
        ]
    case _:
        border_focus = "#881111"
        border_normal = "#220000"
        this_screen_tag = "#FF5555"
        other_screen_tag = "#77DDDD"
        bar_height = 25
        bar_background = "#00000000"
        floating_border_focus = "#0000FF"
        floating_border_default = "#000022"
        rofi_theme = "oni"
        strict_workspaces = False
        strict_map = []

defaults = {
    "font": "mono",
    "fontsize": 15,
    "gap": 0, #gap between windows
    "border_focus": border_focus, #color
    "border_normal": border_normal, #color
    "this_screen_tag": this_screen_tag, #color
    "other_screen_tag": other_screen_tag, #color
    "bar_height": bar_height,
    "bar_background": bar_background, #color + opacity
    "floating_border_focus": floating_border_focus, #color
    "floating_border_default": floating_border_default, #color
    "rofi_theme": rofi_theme,
}


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
        self.keymap_location = home + "/keymaps/"
        
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

keyboard_switcher = KeyboardSwitcher(
    configured_keyboards = [
        ("us-enhanced", "us"),
        ("universal", "un"),
        ("colemak-dh", "cm"),
        ("semimak-jq", "sm"),
        ("mtgap", "mt"),
    ]
)
keyboard_switcher.font = defaults['font']
keyboard_switcher.fontsize = defaults['fontsize']



'''
########## HOOKS ##########
'''


@hook.subscribe.startup_once
def autostart():
    """Run at Qtile start"""
    global home 
    initialize_monitors()
    initialize_mouse_positions(monitors)
    subprocess.run([home + "/autorun.sh"], shell = True)

    
@hook.subscribe.startup
def startup():
    """Runs any time Qtile is restarted"""
    initialize_monitors()
    initialize_mouse_positions(monitors)
    subprocess.run([home + "/autorun.sh -r"], shell = True)


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



'''
########## INITIALIZATION FUNCTIONS ##########
'''


def initialize_mouse_positions(monitors: list[tuple[int, int, int, int]]):
    """Initializes mouse position for each screen."""
    global mouse_positions
    mouse_positions = []
    for monitor in monitors:
        mouse_positions.append((monitor[2] + round(monitor[0] / 2), monitor[3] + round(monitor[1] / 2)))


def initialize_strict_workspaces():
    """Turns the strict workspace config into a usable form."""
    global strict_map, strict
    monitors_num = len(subprocess.check_output(['xrandr', '--listmonitors']).splitlines()[1:])
    if monitors_num > len(strict_map): #strict_map doesn't have this num of monitors
        strict = {}
    else:
        strict = strict_map[monitors_num-1]


def extract_resolution(monitor: bytes) -> tuple[int, int, int, int]:
    """Helper function, converts a monitor's string (from xrandr) into a resolution and position."""
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
    """Retrieves monitor resolutions and positions using xrandr."""
    global monitors
    initialize_strict_workspaces()
    monitors_raw = subprocess.check_output(['xrandr', '--listmonitors']).splitlines()[1:]
    monitors = list(map(lambda x: extract_resolution(x.split()[2]), monitors_raw)) #grab string resolution and extract ints
    # subprocess.check_output(["xrandr", "--query"], shell = True)
    # list(filter(lambda x: " connected" in x, x.decode("utf-8").splitlines()))
    temp = subprocess.check_output(['xrandr', '--query'])
    y = list(filter(lambda x: " connected" in x, temp.decode("utf-8").splitlines()))
    if len(monitors) != len(y):
        debug_notif(f"Lengths are not equal! {len(monitors)} vs {len(y)}")



'''
########## TOOL FUNCTIONS ##########
'''


def get_methods(obj) -> list[str]:
    """Look at the methods available for a Python object."""
    return [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]


def debug_notif(message):
    """Shows a notification via dunst"""
    message = str(message).replace("<", '').replace(">", '')
    subprocess.run([f"dunstify --timeout=2000 debug \"{message}\"" ], shell=True)


#def debug_write(message):
#    """Writes into ~/.debug_qtile.txt, deprecated"""
#    with open(home + "/debug_qtile.txt", "w") as file:
#        file.write(str(message))


def reload_autorun(qtile):
    """Reloads autorun.sh"""
    subprocess.run([home + "/autorun.sh --reload"], shell=True)


def get_strict_workspace_screen(qtile, workspace: int) -> int:
    """Get the screen a strict workspace is assigned to. Returns the current screen if none."""
    global strict
    num = strict.get(workspace)
    if num == None:
        mouse_pos = qtile.core.get_mouse_position()
        cur = get_cur_screen(mouse_pos, monitors)
        return cur
    else:
        return num


def mouse_to_screen(qtile, screen: int):
    """Move the mouse to the target screen."""
    global mouse_positions, monitors

    if len(qtile.screens) < 2:
        return

    mouse_pos = qtile.core.get_mouse_position()
    cur = get_cur_screen(mouse_pos, monitors)

    if screen >= len(qtile.screens):
        debug_notif(f"Invalid screen: {screen}")
        return

    mouse_positions[cur] = mouse_pos
    new_pos = mouse_positions[screen]
    subprocess.call(["xdotool", "mousemove", str(new_pos[0]), str(new_pos[1])])
    qtile.cmd_to_screen(screen)


def launch_rstudio(qtile):
    """Launch rstudio within a specific shell. Should be repurposed to be generic."""
    try:
        subprocess.Popen(["nix-shell shells/r.nix --command rstudio"], shell=True) #this works but freezes qtile for a sec
    except Exception as e:
        debug_notif(e)


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
    return -1 #unreachable code


def float_to_front(qtile):
    """Bring all floating windows of the group to front, consider running this with every new instance."""
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


def focus_cur_screen(qtile, update_mouse: bool):
    """Focuses the screen the mouse is on."""
    global mouse_positions

    mouse_pos = qtile.core.get_mouse_position()
    cur = get_cur_screen(mouse_pos, monitors)
    qtile.cmd_to_screen(cur)
    if update_mouse:
        mouse_positions[cur] = mouse_pos
        subprocess.call(["xdotool", "mousemove", str(mouse_pos[0]), str(mouse_pos[1])])


def mouse_cycle_screen(qtile, clockwise: bool):
    """Move the mouse to the next or previous screen. Consider deprecating."""
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
    """Move focused window to next or previous screen, also asks if mouse should follow. Consider deprecating."""
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
        mouse_cycle_screen(qtile, clockwise)
        #debug_write(f"{now_win}, {cur_win}, {qtile.current_window}, {new_win}")
        #qtile.current_window.cmd_focus() #this shit aint working, supposed to focus the moved window
        qtile.cmd_to_screen(target)


def switch_keyboard_layout(qtile, keyboard_switcher: KeyboardSwitcher, clockwise: bool):
    """Switch the keyboard layout."""
    if clockwise:
        keyboard_switcher.left_click()
    else:
        keyboard_switcher.right_click()


def switch_to_workspace(qtile, workspace):
    """Switch to a specific workspace, respecting strict workspaces."""
    if strict_workspaces:
        workspace_num = int(workspace.name)
        target_screen = get_strict_workspace_screen(qtile, workspace_num) #see if it's tied to a screen
        mouse_to_screen(qtile, target_screen)
    focus_cur_screen(qtile, update_mouse = True) #ensure mouse position stays
    qtile.groups[int(workspace.name)-1].cmd_toscreen() #moves the workspace to the current screen #TEST REMOVING cmd_



'''
########## KEYBINDS ##########
'''


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),

    Key([mod], "i", lazy.function(mouse_cycle_screen, clockwise = True), desc="Focus next monitor"),
    Key([mod, "shift"], "i", lazy.function(window_cycle_screen, clockwise = True, switch_screen = True), desc="Follow window to next monitor"),
    Key([mod, "control"], "i", lazy.function(window_cycle_screen, clockwise = True, switch_screen = False), desc="Move window to next monitor"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "space", lazy.spawn(f"rofi -show run -theme {defaults['rofi_theme']}"), desc="Run dmenu"),
    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "o", lazy.spawn("gsimplecal"), desc="Run gsimplecal"),
    Key([mod, alt], "h", lazy.spawn("code"), desc="Run vscode"),
    Key([mod, alt], "j", lazy.spawn("firefox"), desc="Run firefox"),
    Key([mod, alt], "k", lazy.spawn("librewolf"), desc="Run librewolf"),
    Key([mod, alt], "l", lazy.spawn("brave"), desc="Run brave"),
    Key([mod, alt], "n", lazy.spawn("thunar"), desc="Run thunar"),
    Key([mod, alt], "m", lazy.spawn("kitty -e lf"), desc="Run lf"),
    #Key([mod, alt], "y", lazy.spawn("flatpak run com.mojang.Minecraft"), desc="Run minecraft"),
    Key([mod, alt], "u", lazy.spawn("spotify"), desc="Run spotify"),
    Key([mod, alt], "i", lazy.spawn("discord"), desc="Run discord"),
    Key([mod, alt], "o", lazy.spawn("easyeffects"), desc="Run easyeffects"),
    #Key([mod, alt], "p", lazy.function(launch_rstudio), desc="Run rstudio"),

    Key([mod], "F1", lazy.spawn("systemctl poweroff"), desc="Shutdown"),
    Key([mod], "F2", lazy.spawn("systemctl reboot"), desc="Restart"),
    Key([mod], "F3", lazy.shutdown(), desc="Logout / Shutdown Qtile"),
    Key([mod], "F4", lazy.spawn("systemctl suspend"), desc="Sleep"),

    Key([mod, "shift"], "z", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "s", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod], "slash", lazy.function(float_to_front), desc="Bring all floating windows forward"),
    #Key([mod], "comma", lazy.window.toggle_minimize(), desc="Toggle minimize"),

    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "b", lazy.function(reload_autorun), desc="Fix config things, run autorun.sh again"),
    Key([mod], "d", lazy.function(switch_keyboard_layout, keyboard_switcher, clockwise = False), desc="Previous keyboard layout"),
    Key([mod], "f", lazy.function(switch_keyboard_layout, keyboard_switcher, clockwise = True), desc="Next keyboard layout"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    #Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod], "Next", lazy.spawn("redshift -P -O 6500"), desc="Redshift 0"),
    Key([mod], "Prior", lazy.spawn("redshift -P -O 3500"), desc="Redshift 1"),
    Key([mod], "KP_Up", lazy.spawn("brightnessctl set 10%+"), desc="Brightness up"),
    Key([mod, "shift"], "KP_Up", lazy.spawn("brightnessctl set 1%+"), desc="Brightness slight up"),
    Key([mod], "KP_Down", lazy.spawn("brightnessctl set 10%-"), desc="Brightness down"),
    Key([mod, "shift"], "KP_Down", lazy.spawn("brightnessctl set 1%-"), desc="Brightness slight down"),
    Key([mod, "control"], "KP_Down", lazy.spawn("redshift -P -O 6500"), desc="Redshift 0"),
    Key([mod, "control"], "KP_Up", lazy.spawn("redshift -P -O 3500"), desc="Redshift 1"),
    Key([mod, "control"], "KP_Left", lazy.spawn("redshift -P -O 2500"), desc="Redshift 2"),
    Key([mod, "control"], "KP_Right", lazy.spawn("redshift -P -O 1500"), desc="Redshift 3"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    #Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
]

groups = [Group(i) for i in "1234567890"]


#def window_to_group(qtile, workspace, follow: bool):
#    if not follow: #just move window over there
#        qtile.cmd_togroup(workspace.name, switch_group = False)
#    elif strict_workspaces: #following and respecting strict workspaces
#        workspace_num = int(workspace.name)
#        target_screen = get_strict_workspace_screen(qtile, workspace_num) #see if it's tied to a screen
#        qtile.cmd_togroup(workspace.name, switch_group = False) #moves the workspace to the current screen
#        mouse_to_screen(qtile, target_screen)
#        focus_cur_screen(qtile, update_mouse = True) #ensure mouse position stays
#    else: #following without respecting strict workspaces
#        debug_notif("a")
#        #qtile.cmd_togroup(workspace.name, switch_group = True) #moves the workspace to the current screen
#        qtile.current_window.togroup(qtile.groups[i + 1].name)
#        debug_notif("b")
#qtile.current_screen.set_group(qtile.groups_map[SOMETHING])
#qtile.current_screen.index
#qtile.groups_map[name].toscreen() #brings a workspace to this screen


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.function(switch_to_workspace, workspace = i), desc="Switch to group {}".format(i.name)),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group = True), desc="Switch to & move focused window to group {}".format(i.name)),
            # Or, use below if you prefer not to switch to that group.
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group = False), desc="Move focused window to group {}".format(i.name)),

            Key([mod, alt], i.name, lazy.function(swap_workspaces, target = i), desc="Swaps two workspaces"),
            Key([mod, alt, "control"], i.name, lazy.function(all_to_workspace, target = i), desc=f"Moves all current windows to workspace {i.name}"),
        ]
    )


layouts = [
    layout.Columns(
        #border_focus_stack=["#d75f5f", "#8f3d3d"],
        #border_focused = "#881111",
        #border_focus = "#5294e2",
        #border_focus = "#2222BB",
        #border_focus = "#5fafff",

        border_focus = defaults["border_focus"],
        border_normal = defaults["border_normal"],

        #border_focus = "#2254e2",
        #border_normal = "#000022",
        ##220000, #881111
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
    #layout.Bsp(),
    # layout.Matrix(),
    #layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    #layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

#extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Gap(defaults["gap"]),
        left=bar.Gap(defaults["gap"]),
        right=bar.Gap(defaults["gap"]),
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'] + (2 if hostname == "CobaltCanidPC" else 0),
                    
                    highlight_method = "line",
                    highlight_color = ["#464646FF", "#464646FF"], #gradient
                   
                    block_highlight_text_color = None, #font color for focused workspaces 
                    active = "#FFFFFF",     #font color for workspaces with windows
                    inactive = "#767676",   #font color for workspaces without windows, always affects this focused tab when other screen focused
                    
                    #this_current_screen_border = "#5fafff",     #highlight current screen when current screen in focus
                    this_current_screen_border = defaults["this_screen_tag"],     #highlight current screen when current screen in focus
                    other_screen_border = defaults["other_screen_tag"],            #highlight other screen when current screen in focus
                    
                    this_screen_border = defaults["this_screen_tag"],             #highlight this screen when other screens in focus
                    other_current_screen_border = defaults["other_screen_tag"],    #highlight other screens when other screens in focus
                    
                    disable_drag = True, #disable dragging workspaces around
                    borderwidth = 4, #border of weird things, but affects tag width and highlight height
                ),
                widget.WidgetBox(widgets = [
                    widget.TaskList(
                        #parse_text = lambda _: "",
                    )
                ]),
                widget.Prompt(),
                #widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Spacer(),
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
                widget.Spacer(),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                #widget.GenPollText(
                #    font = defaults['font'],
                #    fontsize = defaults['fontsize'],
                #    update_interval=1,
                #    func=lambda: subprocess.getoutput("ip addr | grep inet | grep enp37s0 | awk '{print $2}'")
                #),
                #widget.Sep(
                #    linewidth = 0,
                #    padding = 6,
                #),
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
                keyboard_switcher, #use the KeyboardSwitcher defined at top of config
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
                        'Button1': lazy.spawn("gsimplecal"),
                    }
                ),
                #widget.QuickExit(),
            ],
            #30,
            defaults["bar_height"],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            #border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            #background = "#282A2EFF",
            #background = "#2A2A2AFF",
            background = defaults["bar_background"],
            margin = [defaults["gap"], 0, 0, 0],
        ),
    ),
    Screen(
        top=bar.Gap(defaults["gap"]),
        left=bar.Gap(defaults["gap"]),
        right=bar.Gap(defaults["gap"]),
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    font = defaults["font"],
                    fontsize = defaults["fontsize"],
                    
                    highlight_method = "line",
                    highlight_color = ["#464646FF", "#464646FF"], #gradient
                   
                    block_highlight_text_color = None, #font color for focused workspaces 
                    active = "#FFFFFF",     #font color for workspaces with windows
                    inactive = "#767676",   #font color for workspaces without windows, always affects this focused tab when other screen focused
                    
                    this_current_screen_border = defaults["this_screen_tag"],     #highlight current screen when current screen in focus
                    other_screen_border = defaults["other_screen_tag"],            #highlight other screen when current screen in focus
                    
                    this_screen_border = defaults["this_screen_tag"],             #highlight this screen when other screens in focus
                    other_current_screen_border = defaults["other_screen_tag"],    #highlight other screens when other screens in focus
                    
                    disable_drag = True, #disable dragging workspaces around
                    borderwidth = 4, #border of weird things, but affects tag width and highlight height
                ),
                widget.TaskList(),
                #widget.Prompt(),
                #widget.WindowName(),
                widget.Spacer(),
                widget.CurrentLayout(
                    font = defaults["font"],
                    fontsize = defaults["fontsize"],
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Clock(
                    font = defaults["font"],
                    fontsize = defaults["fontsize"],
                    format="%m/%d/%Y %a %I:%M %p",
                    mouse_callbacks = {
                        'Button1': lazy.spawn("gsimplecal"),
                    }
                ),
                #widget.QuickExit(),
            ],
            defaults["bar_height"],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background = defaults["bar_background"],
            margin = [defaults["gap"], 0, 0, 0],
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


# Drag floating layouts. EXPERIMENT WITH THIS, SO WINDOWS ARENT FORCED INTO FLOATING
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
    #border_focus = "#5294e2",
    #border_default = "#220000",
    #border_default = "#000022",
    border_focus = defaults["floating_border_focus"],
    border_default = defaults["floating_border_default"],
    #border_width = 1,
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

