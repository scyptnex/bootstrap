#============================================================================#
#                                   bashrc                                   #
#                                                                            #
# Author: nic                                                                #
# Date: 2016-Jun-16                                                          #
#                                                                            #
# This is my bashrc as cobbled together from various sources, mostly the     #
# default one you get with ubuntu, and some of the dotfiles repositories on  #
# github.                                                                    #
#============================================================================#

# Early exit when not being interactive
case $- in
    *i*) ;;
      *) return;;
esac

#===============================#
# Aliases (and hacky functions) #
#===============================#

# ls
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
fi
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# grep
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

#other
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
alias atex="latexmk -pdf -pvc"
alias caly="cal $(date +%Y)"
alias chardump="od -vAn -tax1"
alias cman="man -P \"col -x -b\""
alias colour='for i in {0..255};do printf "%s%3d$(tput sgr0) " "$(tput setab $i)" "$i";if (( i == 15 )) || (( i > 15 )) && (( (i-15) % 6 == 0 )); then echo;fi; done'
alias dat="date +%F_%H:%M"
alias dus='paste <(ls -A | xargs -l1 -d"\n" du -sh | cut -f 1) <(ls -AF) | sort -h'
alias gpgrecipients="gpg --list-only --no-default-keyring --secret-keyring /dev/null"
alias histkill='for I in $(seq $(history | grep "exit$" | tail -n 1 | cut -d" " -f2) $(history | tail -n 1 | cut -d" " -f2) | tac); do history -d $((I+1)); done'
alias latexmk="latexmk -pdf"
alias lucifer="PYTHONPATH=~/project/lucifer/ python3 -m lucifer"
alias lucstat="systemctl status --user lucifer.service; echo ---; systemctl status --user lucifer-sunset.service; echo ---; systemctl status --user lucifer-daylight.service"
alias opn="xdg-open"
alias panda="pandoc -f markdown -o PANDA.pdf"
alias shutup="sudo apt update &&
              sudo apt -y upgrade &&
              sudo apt -y dist-upgrade &&
              sudo apt -y autoremove &&
              sudo apt -y autoclean &&
              echo Shutting down in 10 seconds &&
              sleep 10 &&
              poweroff"

function valias {
    alias $1="echo '$(tput setaf 8)$2$(tput sgr0)';echo;$2"
}
source ~/.bash_aliases

#=======================#
# Environment Variables #
#=======================#

if [ -d $HOME/project/bootstrap/bin ]; then
    export PATH="$PATH:$HOME/project/bootstrap/bin"
fi
if [ -d $HOME/project/ytd/bin ]; then
    export PATH="$PATH:$HOME/project/ytd/bin"
fi
if [ -d $HOME/soft/go ]; then
    export GOROOT="$HOME/soft/go"
    export PATH="$PATH:$GOROOT/bin"
    export GOPATH="$HOME/project/go"
fi
if [ -d $HOME/soft/usr ]; then
    export PATH="$PATH:$HOME/soft/usr/bin"
fi
if [ -d $HOME/.local/bin ]; then
    export PATH="$PATH:$HOME/.local/bin"
fi
export GRADLE_OPTS="-Dorg.gradle.daemon=true"
export EDITOR=vim

if [ -e "$XDG_RUNTIME_DIR/ssh-agent.socket" ]; then
    export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"
fi

# TODO fix this
#- if which gnome-keyring-daemon >/dev/null 2>/dev/null ; then
#-     # Starting the gnome keyring
#-     eval $(/usr/bin/gnome-keyring-daemon --start --components=gpg,pkcs11,secrets,ssh)
#-     export GNOME_KEYRING_CONTROL GNOME_KEYRING_PID GPG_AGENT_INFO SSH_AUTH_SOCK
#- fi

#=========#
# History #
#=========#

HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000

#========#
# Prompt #
#========#

PCOL=0
case "$(hostname)" in
    cpu*)
        PCOL=5
        ;;
    u|dmachine)
        PCOL=6
        ;;
    ghesseraan|Makraan)
        PCOL=2
        ;;
    rpi)
        PCOL=7
        ;;
    Milotic)
        PCOL=38
        ;;
    penguin)
        PCOL=172
        ;;
    ekhtarro)
        PCOL=135
        ;;
    *)
        PCOL=0
        ;;
esac
PS1="\n\[$(tput setaf 8)\][\t] \[$(tput bold)$(tput setaf $PCOL)\]\u@\h: \[$(tput setaf 4)\]\w\[$(tput sgr0)\] \$ "
case "$TERM" in
    # for xterm and alike, set the name of the window
    xterm*|rxvt*)
        PS1="\[\e]0;\u@\h\a\]$PS1"
        ;;
    *)
        ;;
esac

#===========#
# Functions #
#===========#

# Display a man page in vim
function vman(){
    man -P "col -x -b" $@ | vim -R -c 'set ft=man nomod nolist' -c 'map q :q<CR>' -
}

#======#
# Misc #
#======#

# enable programmable completion features
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

shopt -s checkwinsize # check the terminal windo size after commands
#shopt -s globstar

# added by travis gem
[ -f /home/nic/.travis/travis.sh ] && source /home/nic/.travis/travis.sh

[ -f ~/.fzf.bash ] && source ~/.fzf.bash

[ -f ~/.cargo/env ] && . "$HOME/.cargo/env"
