home="${HOME}"


# param1: file name, param2: path from home (optional)
verify_file () {
    if [ -f $home"${2}""/""${1}" ]; then
        #colordiff --unified=0 "./"$1 $home"/"$1
        git diff "./"$1 $home"${2}""/""${1}"
    else
        echo $home"${2}""/"$1 does not exist!
    fi
}


# param1: directory name, param2: path from home (optional)
verify_directory () {
    if [ -d $home"${2}""/""${1}" ]; then
        #git diff "./"$1 $home"${2}""/""${1}"
        #git diff "./"$1 $home"${2}""/""${1}" -- . "':!"$home"${2}""'"
        #git diff --no-index "./"$1 -- $home"${2}""/""${1}" "':!*.pyc'" 
        #git diff --no-index "./"$1 $home"${2}""/""${1}"
        git diff --no-index "./"$1 $home"${2}""/""${1}"
    else
        echo $home"${2}""/""${1}" does not exist!
    fi
}


verify_file ".zshrc-personal"
verify_file "autorun.sh"
verify_file "commands.txt"

verify_directory "keymaps"
verify_directory "shells"

verify_directory "alacritty" "/.config"
verify_directory "awesome" "/.config"
verify_directory "bspwm" "/.config"
verify_directory "Code" "/.config"
verify_directory "copyq" "/.config"
verify_directory "easyeffects" "/.config"
verify_directory "gsimplecal" "/.config"
verify_directory "home-manager" "/.config"
verify_directory "kitty" "/.config"
verify_directory "lf" "/.config"
verify_directory "nixpkgs" "/.config"
verify_directory "nvim" "/.config"
verify_directory "picom" "/.config"
verify_directory "qtile" "/.config"
verify_directory "rofi" "/.config"


