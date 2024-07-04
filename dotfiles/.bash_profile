# Source .bashrc on login shells
if [[ -f ~/.bashrc ]]; then
    source ~/.bashrc
fi

# If we have the work config, source that.
if [[ -f ~/work/work-cfg/bash_profile ]]; then
    source ~/work/work-cfg/bash_profile  
fi
