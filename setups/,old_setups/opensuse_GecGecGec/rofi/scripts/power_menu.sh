options="Sleep\nLogout\nReboot\nShutdown"

# Show menu using rofi
chosen=$(echo -e "$options" | rofi -dmenu -i -p "Power Menu" -theme-str 'window { width: 20%; }')

case $chosen in
    "Sleep")
        systemctl suspend
        ;;
    "Logout")
        pkexec --user root pkill -u $USER
        ;;
    "Reboot")
        systemctl reboot
        ;;
    "Shutdown")
        systemctl poweroff
        ;;
    *)
        ;;
esac


