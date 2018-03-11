#! /usr/bin/env bash

#=========================================================================#
#                             permissions.sh                              #
#                                                                         #
# Author: nic                                                             #
# Date: 2018-Mar-11                                                       #
#                                                                         #
# Options:                                                                #
#   -h           Display this help message                                #
#=========================================================================#

set -e # error on non-zero exit
set -u # undefined variables are an error

function usage(){
    grep "^#.*#$" $0
}

function errxit(){
    [ $# -gt 0 ] && echo "Error: $@" >&2
    echo "Re-run with -h for help" >&2
    exit 1
}

chmod 700 ~/.gnupg/
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa.pub
