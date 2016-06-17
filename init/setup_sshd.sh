#! /usr/bin/env bash

#=========================================================================#
#                              setup_sshd.sh                              #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Jun-17                                                       #
#                                                                         #
# installs and configures sshd with my preferred options                  #
#=========================================================================#

set -e
set -u

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# TODO
# apt-get install openssh-server

cman ssh_config | grep -A 50 Ciphers | grep -A 50 default | grep -v "default" | grep -A 50 "^..*$" | grep -m 1 -B 50 "^$" | tr -d '[:space:]'

