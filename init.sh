#! /usr/bin/env bash

#-------------------------------------------------------------------------#
#                                 init.sh                                 #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Mar-25                                                       #
#                                                                         #
# Sets up the local running ssh files (by getting a temporary copy of ssh #
# ids and sshup.sh script, then checking out a copy of this repository.   #
#-------------------------------------------------------------------------#

function usage(){
    grep "^#.*#$" $0
}

while getopts "h" opt; do
    case $opt in
        h)
            usage
            exit 0
            ;;
        \?)
            usage
            exit 1
            ;;
    esac
done
shift $(($OPTIND -1))

echo $@
