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

from base import *
from bars import screens
from keybinds import keys


# Run at Qtile start
@hook.subscribe.startup_once
def autostart():
    global mouse_positions
    subprocess.run([home + "/autorun.sh"], shell=True)
    
  
# Focus newly spawned windows, not working currently 
#@hook.subscribe.client_managed
#def client_new(client):
#    client.cmd_focus()
#    hook.fire("focus_change") 

@hook.subscribe.client_new
def client_new(client):
    qtile.debug()  # turn on debug logging
    client.focus()
    qtile.warning()  # turn off debug logging

# MARKED FOR UPDATING, refactor this code
# On a new client, spawn on the same screen as the mouse initially, otherwise follow the rules 
@hook.subscribe.client_new
def client_new(client: backend.base.Window):
    global mouse_pynput

    # have newly opening windows respect the mouse position
    #mouse_xpos = qtile.core.get_mouse_position()[0]
    #if mouse_xpos <= 1920:  #NOTE: this must be changed for every monitor
    #    client.cmd_toscreen(0)
    #else:
    #    client.cmd_toscreen(1)
    

    # move windows to their correct workspace
    classes = client.get_wm_class()
    if 'code-oss' in classes or 'jetbrains-rider' in classes:
        client.togroup('1')
    elif 'discord' in classes:
        client.togroup('8')
    elif client.name == None: #workaround for spotify, but may affect other programs too
        client.togroup('9')
    else:
        client.cmd_toscreen(determine_monitor(qtile, mouse_pynput.position))
    
    client.cmd_focus()
    hook.fire("focus_change")


    
    
        
#def mouse_move(qtile):
#    qtile.core._root.set_attribute(eventmask=(EventMask.StructureNotify
#                                            | EventMask.SubstructureNotify
#                                            | EventMask.SubstructureRedirect
#                                            | EventMask.EnterWindow
#                                            | EventMask.LeaveWindow
#                                            | EventMask.ButtonPress
#                                            | EventMask.PointerMotion))
#    def screen_change(event):
#        assert qtile is not None
#        if qtile.config.follow_mouse_focus and not qtile.config.cursor_warp:
#            if hasattr(event, "root_x") and hasattr(event, "root_y"):
#                screen = qtile.find_screen(event.root_x, event.root_y)
#                if screen:
#                    index_under_mouse = screen.index
#                    if index_under_mouse != qtile.current_screen.index:
#                        qtile.focus_screen(index_under_mouse, warp=False)
#        qtile.process_button_motion(event.event_x, event.event_y)
#    setattr(qtile.core, "handle_MotionNotify", screen_change)
#
#@hook.subscribe.startup_once
#def my_func_name():
#    mouse_move(qtile)


#@hook.subscribe.startup_once
#def autostart():
#    processes = [
#        ['/usr/bin/setxkbmap', '-option', 'caps:swapescape'],
#        ['feh', '--bg-scale', '/home/user/Pictures/wallpaper/archfoil.jpg'],
#        ['blueman-applet'],
#        ['nextcloud']
#    ]
#
#    for p in processes:
#        subprocess.Popen(p)





layouts = [
    layout.Columns(
        #border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_focused = "#881111",
        border_normal = "#220000",
        border_width = 2,
        border_on_single = True,
        margin = gap,
        margin_on_single = gap,
        
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
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

#layouts[0].margin = 10 #YOO THIS WORKS

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()



#screens = bars.screens




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
#wmname = "LG3D" #will change back if necessary
wmname = "qtile"
