from base import *

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

    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -M set Master 5%+"), desc="Volume up"),
    Key(["shift"], "XF86AudioRaiseVolume", lazy.spawn("amixer -M set Master 1%+"), desc="Volume slight up"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -M set Master 5%-"), desc="Volume down"),
    Key(["shift"], "XF86AudioLowerVolume", lazy.spawn("amixer -M set Master 1%-"), desc="Volume slight down"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -M set Master toggle"), desc="Volume toggle mute"),

    # Power
    Key([mod], "F1", lazy.spawn("systemctl poweroff"), desc="Shutdown"),
    Key([mod], "F2", lazy.spawn("systemctl reboot"), desc="Restart"),
    Key([mod], "F3", lazy.shutdown(), desc="Logout / Shutdown Qtile"),

    # Close window
    Key([mod, "shift"], "z", lazy.window.kill(), desc="Kill focused window"),

    #Spawn prompt
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"), #if testing config, change this to p temporarily to ensure new config is activated
    
    # Miscellaneous
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    #xdotool key U00D1
    #xdotool key shift+U00D1
    #Key([mod], "slash", float_to_front, desc="Bring all floating windows forward"),
    Key([mod], "slash", lazy.function(float_to_front), desc="Bring all floating windows forward"),
    Key([mod], "q", lazy.function(toggle_rice), desc="Toggle the activation of the rice"),
    
    
]

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

