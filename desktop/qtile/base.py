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

from ricing import gap

home = os.path.expanduser('~')
mouse_pynput = Controller()
mouse_positions = []
floating_window_index = 0
layouts = []

mod = "mod4"
alt = "mod1"
terminal = "kitty"
groups = [Group(i) for i in "1234567890"]


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
    next_screen_index = (screen_index + 1) % len(qtile.screens)
    
    mouse_positions[screen_index] = mouse_pos #save the current mouse position before switching
    
    #switch focus and mouse position
    mouse_pynput.position = mouse_positions[next_screen_index]
    if move_focus == True:
        #NOTE fix this so that it works when switching from an unfocused monitor, currently bugs out
        qtile.cmd_next_screen() #will need to remove the cmd_ in the future
        #qtile.cmd_toscreen(next_screen_index)


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


def float_cycle(qtile, forward: bool):
    global floating_window_index
    floating_windows = []
    for window in qtile.current_group.windows:
        if window.floating:
            floating_windows.append(window)
    if not floating_windows:
        return
    floating_window_index = min(floating_window_index, len(floating_windows) - 1)
    if forward:
        floating_window_index += 1
    else:
        floating_window_index += 1
    if floating_window_index >= len(floating_windows):
        floating_window_index = 0
    if floating_window_index < 0:
        floating_window_index = len(floating_windows) - 1
    win = floating_windows[floating_window_index]
    win.cmd_bring_to_front()
    win.cmd_focus()

def float_cycle_backward(qtile):
    '''
    Cycles to the previous floating window
    '''
    float_cycle(qtile, False)


def float_cycle_forward(qtile):
    '''
    Cycles to the next floating window
    '''
    float_cycle(qtile, True)


def float_to_front(qtile):
    """
    Bring all floating windows of the group to front
    """
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()

def toggle_rice(qtile):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    debug_write(dir_path)
    
    lines = []
    with open(dir_path + "rice_config.txt", "r") as file:
        lines = file.readlines()
    debug_write(lines)
    for i in range(len(lines)):
        if "rice = " in lines[i].strip() and len(lines[i].split()) == 3:
            debug_write('in if')
            setting = "on" if lines[i].split()[2] == "off" else "off"
            lines[i] = f"rice = {setting}\n"
    with open(dir_path + "rice_config.txt", "w") as file:
        file.writelines(lines)
    
    #subprocess.run([f"python {dir_path}ricer.py"], shell = True, start_new_session = True)
    import ricer
    ricer.main()
    qtile.cmd_reload_config()
    
