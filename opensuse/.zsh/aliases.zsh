alias ls='ls --color=auto'
alias la='ls -a --color=auto'
alias ll='ls -lh --color=auto'

alias cp='cp -i'

alias gitconfigp="git config user.name opossalite && git config user.email werbird10@gmail.com"
alias gitconfigw="git config user.name nbalcarc && git config user.email nathan.balcarcel@gmail.com"
alias gitconfigm="git config user.name horprus && git config user.email horprus@proton.me"

alias ff="fastfetch --logo opensuse"

alias py="python3"
alias da="deactivate"

# python (implemented via aliases)
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


