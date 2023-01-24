from base import *

# Open the popup calendar 
def open_calendar(qtile):
    subprocess.run([home + "/.config/qtile/popup-calendar.sh --popup"], shell=True)
    
    
defaults = {
    'font': "mono",
    'fontsize': 14,
}

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
                widget.CheckUpdates(
                    font = defaults['font'],
                    fontsize = defaults['fontsize'],
                    distro = "Arch_yay",
                ),
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
