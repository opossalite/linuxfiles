import os
import subprocess
from libqtile import qtile, hook, backend

import widgets


mouse_positions: list[tuple[int, int]] = []
monitors: list[tuple[int, int, int, int]] = []

home = os.path.expanduser("~")



"""
############ HOOKS ############
"""

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



"""
############ FUNCTIONS ############
"""

#def debug_write(message):
#    """Writes into ~/.debug_qtile.txt"""
#    with open(home + "/debug_qtile.txt", "w") as file:
#        file.write(str(message))


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


def switch_keyboard_layout(qtile, keyboard_switcher: widgets.KeyboardSwitcher, clockwise: bool):
    """Switch the keyboard layout"""
    if clockwise:
        keyboard_switcher.left_click()
    else:
        keyboard_switcher.right_click()




