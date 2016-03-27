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

set -e
set -u

function githubget(){
    wget -O $TMP_DIR/$2 https://github.com/scyptnex/bootstrap/raw/master/$1/$2
}

which git >/dev/null 2>/dev/null || (echo "Install git" >&2 && exit 1)
which openssl >/dev/null 2>/dev/null || (echo "Install openssl" >&2 && exit 1)
REPO_DIR="bootstrap"
TMP_DIR=`mktemp -d`
RSA_FILE="rsa_2048.aes-256-cbc.enc"
# githubget ssh "sshup.sh"
# githubget ssh "$RSA_FILE"
# githubget bin "crypt"
# chmod a+x "$TMP_DIR/sshup.sh"
# chmod a+x "$TMP_DIR/crypt"
# PATH="$PATH:$TMP_DIR" $TMP_DIR/sshup.sh "$TMP_DIR/$RSA_FILE"
# rm -rf $TMP_DIR
# git clone git@github.com:scyptnex/bootstrap.git $REPO_DIR

# linking configurations
for CFG in $REPO_DIR/config/*; do
    if [[ $CFG =~ .*bashrc$ ]] && [ -f $HOME/.bashrc ]; then
        # put the config's bashrc in the current bashrc if it exists and is a file
        sed -i -e '/^\..*bashrc$/d' $HOME/.bashrc
        echo ". `readlink -f $CFG`" >> $HOME/.bashrc
    else
        # remove anythink that is not the proper config and link the config
        rm -f ~/.${CFG#$REPO_DIR/config/}
        ln -s $(readlink -f "$CFG") ~/.${CFG#$REPO_DIR/config/}
    fi
done

