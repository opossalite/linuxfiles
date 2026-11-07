# main place to source everything in this directory

# place this in .zshrc:
# source ~/.zsh/main.zsh

# install zsh and run this:
# chsh -s $(which zsh)


# variables
source ~/.zsh/variables.zsh

# aliases
source ~/.zsh/aliases.zsh

# zsh-autosuggestions           https://github.com/zsh-users/zsh-autosuggestions
source ~/.zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting       https://github.com/zsh-users/zsh-syntax-highlighting
source ~/.zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# zsh-history-substring-search  https://github.com/zsh-users/zsh-history-substring-search
source ~/.zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh

bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# prompt
get-venv() {
    [[ -n "$VIRTUAL_ENV" ]] && echo "($(basename $VIRTUAL_ENV)) "
}
precmd() {
    #PROMPT="%B%F{15}%n%F{10}@%m%F{15}:%F{12}$(dir_abbrev $PWD)%F{15}$%b%f "
    #PROMPT="$(get-venv)%F{10}%n%F{15}@%m %F{10}$(dir_abbrev $PWD)%F{15}>%f "
    PROMPT="$(get-venv)%F{12}%n%F{15}@%m %F{12}$(dir_abbrev $PWD)%F{15}>%f "
}

# bindings
bindkey "^[[H" beginning-of-line
bindkey "^[[F" end-of-line

# path
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/go/bin:$PATH"

export PATH="$HOME/gits/llama.cpp/build/bin:$PATH"

# run
#echo hi
#fastfetch --logo-color-2 000000
#fastfetch --logo-type nones
#fastfetch --structure os:host:kernel:uptime:packages:shell:display:wm:cursor:terminal:terminalfont:cpu:gpu:memory:swap:disk:localip:battery:locale
#fastfetch --structure title:separator:os:host:kernel:uptime:packages:shell:display:wm:cursor:cpu:gpu:memory:swap:disk:localip:battery:locale
#fastfetch --structure
#echo "You're on NixOS, bitch!" | cowsay
#echo ""
python3 ~/.zsh/scripts/cowsay-logo.py

