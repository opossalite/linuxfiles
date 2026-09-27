#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias py=python
alias py39=python3.9

#COLOR="\[$(tput setaf 241)\]"
DARKRED="\[$(tput setaf 1)\]"
#TURQUOISE="\[$(tput setaf 6)\]"
#RED="\[$(tput setaf 9)\]"
#LIME="\[$(tput setaf 10)\]"
#GREYBLUE="\[$(tput setaf 12)\]"
#TEAL="\[$(tput setaf 14)\]"
WHITE="\[$(tput setaf 15)\]"
DARKGREY="\[$(tput setaf 240)\]"
#LIGHTGREY="\[$(tput setaf 247)\]"
BOLD="\[$(tput bold)\]"
RESET="\[$(tput sgr0)\]"

#PS1='[\u@\h \W]\$ '
#. "$HOME/.cargo/env"

#PS1="${COLOR}prompt${RESET}>"

PS1="${BOLD}${DARKRED}[${WHITE}\u@\h ${DARKGREY}\W${DARKRED}]${WHITE}$ ${RESET}"
. "$HOME/.cargo/env"

[ -f "/home/terrior/.ghcup/env" ] && source "/home/terrior/.ghcup/env" # ghcup-env
eval "$(thefuck --alias)"
