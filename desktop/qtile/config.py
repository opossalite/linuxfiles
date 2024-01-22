import os
import subprocess
from libqtile import qtile, bar, layout, widget, hook, backend
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import widgets
from functions import *


home = os.path.expanduser("~")
mod = "mod4"
alt = "mod1"

groups = [Group(i) for i in "1234567890"]
mappings = [(0 if i < 6 else 1) for i in range(0, 10)] #screen 0: 1-6, screen 1: 7-0
if len(groups) != len(mappings): #failsafe
    debug_notif("groups and mappings don't match in length!")
    mappings = [0] * len(groups)

widget_defaults = dict(
    font = "sans",
    fontsize = 12,
    padding = 3,
)
defaults = {
    "font": "mono",
    "fontsize": 15,
}

keyboard_switcher = widgets.KeyboardSwitcher(
    configured_keyboards = [
        #("us", "us"),
        ("us-enhanced", "us"),
        ("es", "es"),
        ("universal", "un"),
        ("colemak-dha", "cm"),
        ("semimak-jq", "sm"),
        ("mtgap", "mt"),
        ("us-programmer", "up"),
        #("us-enhanced", "ue"),
    ]
)
keyboard_switcher.font = defaults['font']
keyboard_switcher.fontsize = defaults['fontsize']


keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod], "i", lazy.function(mouse_cycle_screen, clockwise=True), desc="Focus next monitor"),
    Key([mod, "shift"], "i", lazy.function(window_cycle_screen, clockwise=True, switch_screen=True), desc="Follow window to next monitor"),
    Key([mod, "control"], "i", lazy.function(window_cycle_screen, clockwise=True, switch_screen=False), desc="Move window to next monitor"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "comma", lazy.window.toggle_minimize(), desc="Toggle minimize"),
    #Key([mod], "comma", lazy.window.toggle_, desc="Restart"),

    Key([mod], "Return", lazy.spawn("kitty"), desc="Launch terminal"),
    Key([mod], "space", lazy.spawn("rofi -show run -theme oni"), desc="Run rofi"),
    Key([mod], "o", lazy.spawn("gsimplecal"), desc="Run gsimplecal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "s", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "shift"], "z", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Logout / Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "b", lazy.spawn("nitrogen --restore"), desc="Restart background"),

    #Key([mod, alt], "h", lazy.spawn("codium"), desc="Run vscodium"),
    Key([mod, alt], "h", lazy.spawn("code"), desc="Run vscode"),
    Key([mod, alt], "j", lazy.spawn("firefox"), desc="Run firefox"),
    Key([mod, alt], "k", lazy.spawn("librewolf"), desc="Run librewolf"),
    Key([mod, alt], "l", lazy.spawn("brave"), desc="Run brave"),
    Key([mod, alt], "n", lazy.spawn("thunar"), desc="Run thunar"),
    Key([mod, alt], "m", lazy.spawn("kitty -e lf"), desc="Run lf"),
    Key([mod, alt], "y", lazy.spawn("flatpak run com.mojang.Minecraft"), desc="Run minecraft"),
    Key([mod, alt], "u", lazy.spawn("spotify"), desc="Run spotify"),
    Key([mod, alt], "i", lazy.spawn("discord"), desc="Run discord"),
    Key([mod, alt], "o", lazy.spawn("easyeffects"), desc="Run easyeffects"),

    # Keyboard Layouts
    Key([mod], "d", lazy.function(switch_keyboard_layout, keyboard_switcher, clockwise = False), desc="Previous keyboard layout"),
    Key([mod], "f", lazy.function(switch_keyboard_layout, keyboard_switcher, clockwise = True), desc="Next keyboard layout"),

    # Power
    Key([mod], "F1", lazy.spawn("systemctl poweroff"), desc="Shutdown"),
    Key([mod], "F2", lazy.spawn("systemctl reboot"), desc="Restart"),
    Key([mod], "F3", lazy.shutdown(), desc="Logout / Shutdown Qtile"),
    Key([mod], "F4", lazy.spawn("systemctl suspend"), desc="Sleep"),

    Key([mod], "slash", lazy.function(float_to_front), desc="Bring all floating windows forward"),
    Key([mod], "Next", lazy.spawn("redshift -P -O 6500"), desc="Redshift 0"),
    Key([mod], "Prior", lazy.spawn("redshift -P -O 3500"), desc="Redshift 1"),
    Key([mod, "shift"], "f", lazy.spawn("xset r rate 330 25"), desc="Fix keyboard rate"),
]


groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group = True), desc=f"Switch to & move focused window to group {i.name}"),
            # Or, use below if you prefer not to switch to that group.
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "control"], i.name, lazy.window.togroup(i.name), desc="Move focused window to group {}".format(i.name)),

            Key([mod, alt], i.name, lazy.function(swap_workspaces, target = i), desc="Swaps two workspaces"),
            Key([mod, alt, "control"], i.name, lazy.function(all_to_workspace, target = i), desc=f"Moves all current windows to workspace {i.name}"),
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

gap = 0

extension_defaults = widget_defaults.copy()


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
                widget.WidgetBox(widgets = [
                    widget.TaskList(
                        parse_text = lambda _: "",

                    ),
                ]),
                widget.Prompt(),
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
                widget.CurrentLayout(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                ),
                keyboard_switcher,
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
                widget.TaskList(),
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
                        'Button1': lazy.spawn("gsimplecal"),
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
        #Match(title="Edit Text"),  # krita popup
        #Match(lambda x: x == "a"),  # krita popup
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

