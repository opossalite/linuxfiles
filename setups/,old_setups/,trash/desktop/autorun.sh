#!/usr/bin/env bash

#sxhkd &
#xdg-mime default librewolf.desktop x-scheme-handler/http &
#xdg-mime default librewolf.desktop x-scheme-handler/https &


# devices
#xrandr --output DisplayPort-2 --primary --mode 1920x1080 --rate 165 --output HDMI-A-0 --right-of DisplayPort-2 --mode 1280x1024 --rate 75 &
#xrandr --output DP-0 --primary --mode 1920x1080 --rate 165 --output HDMI-0 --right-of DP-0 --mode 1280x1024 --rate 75 &
#xrandr --output HDMI-0 --primary --mode 1920x1200 --rate 60 &
#xrandr --output HDMI-0 --primary --mode 1920x1200 --rate 60 --output DP-5 --right-of HDMI-0 --mode 1280x1024 --rate 75 &
#xrandr --output DP-5 --primary --mode 1920x1200 --rate 60 --output DP-1 --right-of DP-5 --mode 1280x1024 --rate 75 &
#xrandr --output DP-5 --primary --mode 1920x1200 --rate 60 --output DP-1 --mode 1280x1024 --rate 75 --pos 1920x176
#xrandr --output DP-4 --primary --mode 1920x1080 --rate 165 --output DP-1 --mode 1280x1024 --rate 75 --pos 1920x176
#xrandr --output DP-4 --primary --mode 1920x1080 --rate 165 --output DP-1 --mode 1280x1024 --rate 75
xrandr --output DP-4 --primary --mode 1920x1080 --rate 165 --output HDMI-0 --mode 1280x1024 --rate 75
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "SINOWEALTH Wired Gaming Mouse" "libinput Accel Speed" 0 &
xinput set-prop "Logitech MX Vertical" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "Logitech MX Vertical" "libinput Accel Speed" 0 &
xkbcomp -w 0 ~/.keymaps/us-enhanced.xkb :0 &
xset r rate 330 25 &


# background
picom -b &
nitrogen --restore &
easyeffects --gapplication-service &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# system tray
nm-applet &
pasystray --notify=none --notify=systray_action -m 100 &
copyq &
flameshot &
