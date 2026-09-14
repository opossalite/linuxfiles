# add nice colors to ls
alias ls='ls --color=auto'
alias la='ls -a --color=auto'
alias ll='ls -lh --color=auto'

# reduce mistakes
alias cp='cp -i'

# git stuff
alias gitconfigp="git config user.name opossalite && git config user.email werbird10@gmail.com"
alias gitconfigw="git config user.name nbalcarc && git config user.email nathan.balcarcel@gmail.com"
alias gitconfigm="git config user.name horprus && git config user.email horprus@proton.me"

# devices
alias honeypot="ssh beekeeper@192.168.88.88"
#alias pepsi-zero="ssh terrior@192.168.88.50"
alias pepsi-zero="ssh terrior@pepsi-zero"
alias coke-zero="ssh terrior@192.168.88.51"

# niri equivalent of xprop
#alias niri-prop="sleep 1; niri msg focused-window"
alias niri-prop="niri msg pick-window"

# easy nemo terminal switcher, just append the name of the terminal at the end
alias nemo-set-terminal="gsettings set org.cinnamon.desktop.default-applications.terminal exec"

# use bat instead of cat if available
##cat() {
##    if command -v bat >/dev/null 2>&1; then
##        bat "$@"
##    else
##        command cat "$@"
##    fi
##}


# python stuff
alias py="python3"
alias da="deactivate"

# python plugins (implemented via aliases)
pyv() {
    keywords_py=("new" "rm" "remove" "mv" "rename" "move" "ls" "list")
    keywords_da=("da" "deactivate")
    if [[ " $1 " =~ "  " ]]; then
        echo "Keywords: "$keywords_py
    elif [[ " ${keywords_py[@]} " =~ " $1 " ]]; then
        mkdir ~/.pyv
        python3 ~/.zsh/scripts/pyv.py $*
    elif [[ " ${keywords_da[@]} " =~ " $1 " ]]; then
        deactivate
    else
        source $HOME"/.pyv/"$1"/bin/activate"
    fi
}
alias dir_abbrev="python3 ~/.zsh/scripts/dir_abbrev.py"

