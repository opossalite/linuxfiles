# Created by newuser for 5.9
[[ -f ~/.zshrc-personal ]] && . ~/.zshrc-personal

for f in ~/.zsh/*.sh; do
  . "$f" 
done


