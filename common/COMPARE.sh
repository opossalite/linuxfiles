home="${HOME}"


verify_file () {
    if [ -f $home"/""${1}" ]; then
        #colordiff --unified=0 "./"$1 $home"/"$1
        git diff "./"$1 $home"/""${1}"
    else
        echo $home"/"$1 does not exist!
    fi
}


verify_directory () {
    if [ -d $home"/""${1}" ]; then
        #colordiff --unified=0 "./"$1 $home"/"$1
        git diff "./"$1 $home"/""${1}"
    else
        echo $home"/"$1 does not exist!
    fi
}


verify_directory_config () {
    if [ -d $home"/.config/""${1}" ]; then
        #colordiff --unified=0 "./"$1 $home"/.config/"$1
        git diff "./"$1 $home"/.config/""${1}"
    else
        echo $home"/"$1 does not exist!
    fi
}


verify_file ".zshrc-personal"
verify_file "autorun.sh"
verify_file "commands.txt"

verify_directory "keymaps"
verify_directory "shells"

verify_directory_config "alacritty"
verify_directory_config "awesome"
verify_directory_config "bspwm"
verify_directory_config "Code - OSS"
verify_directory_config "copyq"
verify_directory_config "easyeffects"
verify_directory_config "gsimplecal"
verify_directory_config "home-manager"
verify_directory_config "kitty"
verify_directory_config "lf"
verify_directory_config "nixpkgs"
verify_directory_config "nvim"
verify_directory_config "picom"
verify_directory_config "qtile"
verify_directory_config "rofi"


