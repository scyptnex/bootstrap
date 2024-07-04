# Like xargs but 1 execution per input line
valias largs 'xargs -L1 -d"\n"'

# Print all processes belonging to me
valias psu 'ps -u $(whoami)'

# In work configurations, also include work-specific ones
if [[ -f ~/work/work-cfg/bash_aliases ]]; then
	source ~/work/work-cfg/bash_aliases
fi
