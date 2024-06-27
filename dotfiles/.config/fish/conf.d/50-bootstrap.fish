#---------#
# Aliases #
#---------#

function valias --description "Verbose alias, prints its command"
    alias $argv[1] "set_color brblack;echo '$argv[1] -> $argv[2]';set_color normal;echo;"$argv[2]
end

# Fish-specific aliases go here
valias dus 'paste (ls -A | xargs -l1 -d"\n" du -sh | cut -f 1 | psub) (ls -AF | psub) | sort -h'

# Combined aliases (shared with bash) live here
source ~/.bash_aliases

#-------#
# Paths #
#-------#

if [ -d ~/project/bootstrap/bin ]
    set -g PATH $PATH ~/project/bootstrap/bin
end
