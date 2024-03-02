
# run every time the script is run
if [[ $1 == "-r" || $1 == "--reload" ]]; then
    echo "Reloading"
    # don't do anything special for reloading
else
    echo "Starting"

    # applications
    #easyeffects --gapplication-service &

    #system tray
    nm-applet &
    pasystray --notify=none --notify=systray_action -g -m 100 &
    copyq &
    #klipper &
    flameshot &
    xhost + &

    if [[ $HOSTNAME == "CobaltCanidPC" ]]; then
        picom -b &
        cbatticon -n &
    else
        picom --experimental-backends -b &
    fi
fi


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

# background
num_monitors=$(xrandr --query | grep " connected" | wc -l)
echo $num_monitors

if [[ $num_monitors == "1" ]]; then # ONE MONITOR
    echo "One monitor!"
    case $HOSTNAME in
        ("VulpesKrovPC")
            xrandr --auto
            feh --bg-fill ~/gits/linuxfiles/wallpapers/nix-wallpaper-mine.png &
            ;;

        ("CobaltCanidPC")
            xrandr --auto
            #laptop: xrandr --output eDP-1 --primary --mode 1920x1080 --rate 60 --output HDMI-1 --mode 1920x1080 --rate 60 --above eDP-1
            #xrandr --output eDP-1 --primary --mode 1920x1080 --rate 60 --output HDMI-1 --mode 1920x1080 --rate 60 --above eDP-1
            #feh --bg-fill ~/gits/linuxfiles/wallpapers/blue.png &
            feh --bg-fill ~/gits/linuxfiles/wallpapers/nix-wallpaper-mine.png &
            ;;

        (*)
            echo "Where tf are we!"
            xrandr --auto
            # no background if we don't know what pc we're on
            ;;
    esac
else # MULTIPLE MONITORS
    echo "Multiple monitors!"
    case $HOSTNAME in
        ("VulpesKrovPC")
            xrandr --output DP-4 --primary --mode 1920x1080 --rate 165 --output HDMI-0 --mode 1280x1024 --rate 75
            feh --bg-fill ~/gits/linuxfiles/wallpapers/nix-wallpaper-mine.png ~/gits/linuxfiles/wallpapers/nix-wallpaper-mine.png &
            ;;

        ("CobaltCanidPC")
            xrandr --output eDP-1 --primary --mode 1920x1080 --rate 60 --output HDMI-1 --mode 1920x1080 --rate 60 --above eDP-1
            feh --bg-fill ~/gits/linuxfiles/wallpapers/blue.png ~/gits/linuxfiles/wallpapers/minimalism-ai-art-simple-background-landscape-mountains-night-2202267-wallhere.com.jpg &
            ;;

        (*)
            echo "Where tf are we!"
            echo $HOST
            echo $HOSTNAME
            xrandr --auto
            # no background if we don't know what pc we're on
            ;;
    esac
fi



#settings
xset r rate 330 25 &
xkbcomp -w 0 ~/.keymaps/us-enhanced.xkb :0 & #handles caps_lock underscore
#xmodmap ~/.Xmodmap & #used to handle caps_lock underscore

if [[ $HOST == "CobaltCanidPC" ]]; then
    libinput-gestures &
fi





