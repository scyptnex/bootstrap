# Like xargs but 1 execution per input line
valias largs 'xargs -L1 -d"\n"'

# Play A Random Album
valias para 'mpc clear && beet random -aep | sed "s@^/home/nic/Music/@@" | mpc -vv add && mpc playlist && mpc play'

# Print all processes belonging to me
valias psu 'ps -u $(whoami)'

# Rsync with saneish defaults
valias rsync-r-p 'rsync --recursive --progress --human-readable'
