#---------#
# Aliases #
#---------#

function valias --description "Verbose alias, prints its command"
    alias $argv[1] "set_color brblack;echo '$argv[1] -> $argv[2]';set_color normal;echo;"$argv[2]
end

valias psu "ps -u (whoami)"
valias dus 'paste (ls -A | xargs -l1 -d"\n" du -sh | cut -f 1 | psub) (ls -AF | psub) | sort -h'
valias largs 'xargs -L1 -d"\n"'

#-------#
# Paths #
#-------#

if [ -d ~/project/bootstrap/bin ]
    set -g PATH $PATH ~/project/bootstrap/bin
end
