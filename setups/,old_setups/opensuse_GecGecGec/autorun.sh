#!/bin/bash



# devices; in order: reverse scroll direction, disable acceleration, decrease scroll speed, increase sensitivity
#desktop: xrandr --output DP-4 --primary --mode 1920x1080 --rate 165 --output HDMI-0 --mode 1280x1024 --rate 75
#laptop: xrandr --output eDP-1 --primary --mode 1920x1080 --rate 60 --output HDMI-1 --mode 1920x1080 --rate 60 --above eDP-1
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Speed" 0 &
xinput set-prop "pointer:Logitech MX Vertical" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "pointer:Logitech MX Vertical" "libinput Accel Speed" 0 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Natural Scrolling Enabled" 1 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Scrolling Pixel Distance" 50 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Accel Speed" 0.5 &
xinput set-prop "Logitech G203 LIGHTSYNC Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "Logitech G203 LIGHTSYNC Gaming Mouse" "libinput Accel Speed" 0 &
xinput set-prop "pulsar X2 V2 Mini" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "pulsar X2 V2 Mini" "libinput Accel Speed" 0 &



xset r rate 330 25 &
xkbcomp -w 0 ~/keymaps/us-enhanced.xkb :0 & #handles caps_lock underscore


