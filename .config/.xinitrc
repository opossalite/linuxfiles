sxhkd &
# in order: reverse scroll direction, disable acceleration, decrease scroll speed, increase sensitivity
xinput set-prop 11 "libinput Natural Scrolling Enabled" 1 &
xinput set-prop 11 "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop 11 "libinput Scrolling Pixel Distance" 50 &
xinput set-prop 11 "libinput Accel Speed" 0.5 &
xinput set-prop 10 "libinput Natural Scrolling Enabled" 1 &
xinput set-prop 10 "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop 10 "libinput Scrolling Pixel Distance" 50 &
xinput set-prop 10 "libinput Accel Speed" 0.5 &
xinput set-prop 17 "libinput Accel Profile Enabled" 0, 1 &
xinput set-prop 17 "libinput Accel Speed" 0.5 &
exec bspwm
