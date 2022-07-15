DARKRED="\[$(tput setaf 1)\]"
WHITE="\[$(tput setaf 15)\]"
DARKGREY="\[$(tput setaf 240)\]"
BOLD="\[$(tput bold)\]"
RESET="\[$(tput sgr0)\]"

PS1="${BOLD}${DARKRED}[${WHITE}\u@\h ${DARKGREY}\W${DARKRED}]${WHITE}$ ${RESET}"


