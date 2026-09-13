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

# niri equivalent of xprop
#alias niri-prop="sleep 1; niri msg focused-window"
alias niri-prop="niri msg pick-window"

# easy nemo terminal switcher, just append the name of the terminal at the end
alias nemo-set-terminal="gsettings set org.cinnamon.desktop.default-applications.terminal exec"

# use bat instead of cat if available
cat() {
    if command -v bat >/dev/null 2>&1; then
        bat "$@"
    else
        command cat "$@"
    fi
}


# python stuff
alias py="python3"
alias da="deactivate"

# python plugins (implemented via aliases)
pyv() {
    keywords_py=("new" "rm" "remove" "mv" "rename" "move" "ls" "list")
    keywords_da=("da" "deactivate")
    if [[ " ${keywords_py[@]} " =~ " $1 " ]]; then
        python3 ~/.zsh/python/pyv.py $*
    elif [[ " ${keywords_da[@]} " =~ " $1 " ]]; then
        deactivate
    else
        source $HOME"/.pyv/"$1"/bin/activate"
    fi
}
alias dir_abbrev="python3 ~/.zsh/python/dir_abbrev.py"

