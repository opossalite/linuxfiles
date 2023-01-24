#!/bin/bash

#devices
xrandr --output DisplayPort-2 --primary --mode 1920x1080 --rate 165 --output HDMI-A-0 --right-of DisplayPort-2 --mode 1280x1024 --rate 75 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Speed" 0 &

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


