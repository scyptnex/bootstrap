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
alias chardump="od -vAn -tax1"
alias cman="man -P \"col -x -b\""
alias dat="date +%F-%H:%M"
alias gpgrecipients="gpg --list-only --no-default-keyring --secret-keyring /dev/null"
alias latexmk="latexmk -pdf"
alias atex="latexmk -pdf -pvc"
alias opn="xdg-open"
alias panda="pandoc -f markdown -o PANDA.pdf"

#=======================#
# Environment Variables #
#=======================#

if [ -d $HOME/bootstrap/bin ]; then
    export PATH="$PATH:$HOME/bootstrap/bin"
fi
if [ -d $HOME/soft/go ]; then
    export GOROOT="$HOME/soft/go"
    export PATH="$PATH:$GOROOT/bin"
    export GOPATH="$HOME/project/go"
fi
export GRADLE_OPTS="-Dorg.gradle.daemon=true"

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
    plang*)
        PCOL=6
        ;;
    ghesseraan|Makraan)
        PCOL=2
        ;;
    Therauvra)
        PCOL=7
        ;;
    *)
        PCOL=0
        ;;
esac
PS1="\n\[$(tput bold)$(tput setaf $PCOL)\]\u@\h: \[$(tput setaf 4)\]\w\[$(tput sgr0)\] \$ "
case "$TERM" in
    # for xterm and alike, set the name of the window
    xterm*|rxvt*)
        PS1="\[\e]0;\u@\h\a\]$PS1"
        ;;
    *)
        ;;
esac

#=============#
# SSH Servers #
#=============#

export SSH_C0="nhol8058@cpu0.it.usyd.edu.au"
export SSH_C1="nhol8058@cpu1.it.usyd.edu.au"
export SSH_C2="nhol8058@cpu2.it.usyd.edu.au"
export SSH_BS="nic@plang8.cs.usyd.edu.au"
export SSH_UNI="nic@ghesseran.it.usyd.edu.au"

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

