#!/usr/bin/env bash

# Power menu using fuzzel
# Options
options=(
    "  Sleep"
    "  Log Out"
    "  Lock"
    "  Restart"
    "  Shutdown"
)

# Show menu
choice=$(printf "%s\n" "${options[@]}" | fuzzel --dmenu --prompt "Power Menu: ")

case "$choice" in
*Lock)
    swaylock
    ;;
*Sleep)
    systemctl suspend
    ;;
*Restart)
    systemctl reboot
    ;;
*Shutdown)
    systemctl poweroff
    ;;
*"Log Out")
    # Works for most Wayland compositors using systemd-logind
    loginctl terminate-user "$USER"
    ;;
*)
    exit 0
    ;;
esac
