#!/bin/sh

BAR_HEIGHT=20  # polybar height
BORDER_SIZE=2  # border size from your wm settings
YAD_WIDTH=222  # 222 is minimum possible value
YAD_HEIGHT=193 # 193 is minimum possible value
DATE="$(date +"%a %d %H:%M")"

case "$1" in --popup)
    if [[ "$(xdotool search -name yad-calendar)" ]]; then
	#$(xprop -name yad-calendar _NET_WM_PID | awk '{print $3}' | kill )
	$(kill $(xprop -name yad-calendar _NET_WM_PID | awk '{print $3}'))
	exit 0
    fi

    if [ "$(xdotool getwindowfocus getwindowname)" = "yad-calendar" ]; then
        exit 0
    fi

    eval "$(xdotool getmouselocation --shell)"
    eval "$(xdotool getdisplaygeometry --shell)" #doesn't work for mult monitors
    # GAPS=$(awk '{ print $3}' rice_config.txt)

    if [ $X -gt 1920 ]; then
	: $((pos_x = 220 - YAD_WIDTH)) #second monitor
	: $((pos_y = 130 - YAD_HEIGHT - BAR_HEIGHT))
# 	: $(dunstify "gt $X")
    else
	: $((pos_x = WIDTH - YAD_WIDTH - 30)) #main monitor
	: $((pos_y = HEIGHT - YAD_HEIGHT - BAR_HEIGHT - 28))
#	: $(dunstify "lt $X")
    fi
    echo "hi"
    yad --calendar --undecorated --fixed --close-on-unfocus --no-buttons \
        --width="$YAD_WIDTH" --height="$YAD_HEIGHT" --posx="$pos_x" --posy="$pos_y" \
        --title="yad-calendar" --borders=0 >/dev/null &
    ;;
*)
    echo "$DATE"
    ;;
esac



#case "$1" in
#--popup)
#    if [ "$(xdotool getwindowfocus getwindowname)" = "yad-calendar" ]; then
#        exit 0
#    fi
#
#    eval "$(xdotool getmouselocation --shell)"
#    eval "$(xdotool getdisplaygeometry --shell)"
#
    # X
#    if [ "$((X + YAD_WIDTH / 2 + BORDER_SIZE))" -gt "$WIDTH" ]; then #Right side
#        : $((pos_x = WIDTH - YAD_WIDTH - BORDER_SIZE))
#	: $(dunstify "Right $WIDTH")
#    elif [ "$((X - YAD_WIDTH / 2 - BORDER_SIZE))" -lt 0 ]; then #Left side
#        : $((pos_x = BORDER_SIZE))
#	: $(dunstify "here1")
#    else #Center
#        : $((pos_x = X - YAD_WIDTH / 2))
#	: $(dunstify "Center $X")
#    fi
#
    # Y
#    if [ "$Y" -gt "$((HEIGHT / 2))" ]; then #Bottom
#        : $((pos_y = HEIGHT - YAD_HEIGHT - BAR_HEIGHT - BORDER_SIZE))
#    else #Top
#        : $((pos_y = BAR_HEIGHT + BORDER_SIZE))
#    fi
#
#    yad --calendar --undecorated --fixed --close-on-unfocus --no-buttons \
#        --width="$YAD_WIDTH" --height="$YAD_HEIGHT" --posx="$pos_x" --posy="$pos_y" \
#        --title="yad-calendar" --borders=0 >/dev/null &
#    ;;
#*)
#    echo "$DATE"
#    ;;
#esac
