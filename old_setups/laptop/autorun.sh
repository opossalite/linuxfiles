
# run every time the script is run
if [[ $1 == "-r" || $1 == "--reload" ]]; then
    echo "Reloading"
else
    echo "Starting"

    # applications
    picom --experimental-backends -b &
    easyeffects --gapplication-service &

    #system tray
    nm-applet &
    pasystray --notify=none --notify=systray_action -g -m 100 &
    copyq &
    flameshot &
    cbatticon -n &
fi


# devices; in order: reverse scroll direction, disable acceleration, decrease scroll speed, increase sensitivity
xrandr --output eDP-1 --primary --mode 1920x1080 --rate 60 --output HDMI-1 --mode 1920x1080 --rate 60 --above eDP-1
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Natural Scrolling Enabled" 1 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Scrolling Pixel Distance" 50 &
xinput set-prop "MSFT0001:01 04F3:3140 Touchpad" "libinput Accel Speed" 0.5 &
xinput set-prop "Logitech G203 LIGHTSYNC Gaming Mouse" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "Logitech G203 LIGHTSYNC Gaming Mouse" "libinput Accel Speed" 0 &
xinput set-prop "Logitech MX Vertical" "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop "Logitech MX Vertical" "libinput Accel Speed" 0 &

num_monitors=$(xrandr --query | grep " connected" | wc -l)
echo $num_monitors

# background
if [[ $num_monitors == "1" ]]; then
    echo "One monitor!"
    xrandr --auto
    feh --bg-fill ~/gits/linuxfiles/wallpapers/blue.png &
else
    echo "Multiple monitors!"
    xrandr --output eDP-1 --primary --mode 1920x1080 --rate 60 --output HDMI-1 --mode 1920x1080 --rate 60 --above eDP-1
    feh --bg-fill ~/gits/linuxfiles/wallpapers/blue.png ~/gits/linuxfiles/wallpapers/minimalism-ai-art-simple-background-landscape-mountains-night-2202267-wallhere.com.jpg &
fi


#settings
xset r rate 330 25 &
xmodmap ~/.Xmodmap &
libinput-gestures &







