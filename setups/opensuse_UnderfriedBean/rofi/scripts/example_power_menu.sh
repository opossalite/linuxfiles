#!/bin/bash

# Define menu options
options="Lock\nLogout\nReboot\nShutdown"

# Show menu using rofi
chosen=$(echo -e "$options" | rofi -dmenu -i -p "Power Menu" -theme-str 'window { width: 20%; }')

echo $chosen

## Handle selected option
#case "$chosen" in Lock) # Lock the screen (adjust the command for your locker)
#        #i3lock ;;
#        e
#    Logout)
#        # Logout command (KDE example, replace as needed for your desktop environment)
#        #qdbus org.kde.Shutdown /Shutdown org.kde.Shutdown.logout ;;
#    Reboot)
#        # Reboot the system
#        #systemctl reboot ;;
#    Shutdown)
#        # Shutdown the system
#        #systemctl poweroff ;;
#    *)
#        # Do nothing if no valid option was selected
#        ;;
#esac

