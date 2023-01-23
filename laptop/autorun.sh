#!/bin/bash

#devices
#xrandr --output DisplayPort-2 --primary --mode 1920x1080 --rate 165 --output HDMI-A-0 --right-of DisplayPort-2 --mode 1280x1024 --rate 75 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Speed" 0 &
# in order: reverse scroll direction, disable acceleration, decrease scroll speed, increase sensitivity
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Natural Scrolling Enabled" 1 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Scrolling Pixel Distance" 50 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Accel Speed" 0.5 &

#background
picom -b &
nitrogen --restore &
easyeffects --gapplication-service &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

#system tray
nm-applet &
pasystray -g -m 100 --notify=none --notify=systray_action &
copyq &
dunst &
flameshot &
