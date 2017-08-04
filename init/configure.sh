#! /usr/bin/env bash

#=========================================================================#
#                              configure.sh                               #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Jun-16                                                       #
#                                                                         #
# Create the configurations (dotfiles) as needed                          #
#=========================================================================#

set -e
set -u

REPO_DIR=`readlink -f $(dirname $0)/..`

# HACK1, forcibly remove gnupg configuration
[ -f ~/.gnupg/gpg.conf ] && rm ~/.gnupg/gpg.conf

for IN_F in `find $REPO_DIR/dotfiles/ -type f`; do
    OUT="${IN_F#*${REPO_DIR}/dotfiles/}"
    IN=$(readlink -f "$IN_F")
    mkdir -p $(dirname ~/$OUT)

    # if the file exists, remove symlinks, backup others
    [ -h ~/$OUT ] && rm ~/$OUT
    [ -f ~/$OUT ] && mv ~/${OUT}{,_BACKUP}

    echo "$IN ~/$OUT"
    ln -s "$IN" ~/$OUT
done
