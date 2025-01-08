# main place to source everything in this directory
# git clone _ ~/.zsh/_
# [[ -f ~/.zshrc-personal ]] && source ~/.zshrc-personal

# place this in .zshrc
# source ~/.zsh/main.zsh


# variables
source ~/.zsh/variables.zsh

# aliases
source ~/.zsh/aliases.zsh

# python (implemented via aliases)
alias pyv="python3 ~/.zsh/python/pyv.py"
alias dir_abbrev="python3 ~/.zsh/python/dir_abbrev.py"

# zsh-autosuggestions           https://github.com/zsh-users/zsh-autosuggestions
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting       https://github.com/zsh-users/zsh-syntax-highlighting
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# zsh-history-substring-search  https://github.com/zsh-users/zsh-history-substring-search
source ~/.zsh/zsh-history-substring-search/zsh-history-substring-search.zsh
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# prompt
precmd() {
    #PROMPT="%B%F{15}%n%F{10}@%m%F{15}:%F{12}$(dir_abbrev $PWD)%F{15}$%b%f "
    PROMPT="%F{10}%n%F{15}@%m %F{10}$(dir_abbrev $PWD)%F{15}>%f "
}

# run
fastfetch --logo opensuse


