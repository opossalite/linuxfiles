#!/usr/bin/env bash

#sxhkd &
#xdg-mime default librewolf.desktop x-scheme-handler/http &
#xdg-mime default librewolf.desktop x-scheme-handler/https &


# devices
#xrandr --output DisplayPort-2 --primary --mode 1920x1080 --rate 165 --output HDMI-A-0 --right-of DisplayPort-2 --mode 1280x1024 --rate 75 &
xrandr --output DP-0 --primary --mode 1920x1080 --rate 165 --output HDMI-0 --right-of DP-0 --mode 1280x1024 --rate 75 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Speed" 0 &

# background
picom -b &
nitrogen --restore &
easyeffects --gapplication-service &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# system tray
nm-applet &
pasystray --notify=none --notify=systray_action -g -m 100 &
copyq &
flameshot &
xset r rate 330 25 &
