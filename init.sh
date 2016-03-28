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

# ensure the current shell is bash
# this is a heuristic only, but any user who malliciously set it when not in bash deserves what they get (or asks for it)
if [ "$BASH" == "" ]; then
    echo "Script requires bash (Bourne Again SHell)" >&2
    exit 1
fi

# check that git and openssl exist
which git >/dev/null 2>/dev/null || (echo "Install git" >&2 && exit 1)
which openssl >/dev/null 2>/dev/null || (echo "Install openssl" >&2 && exit 1)

#important variables
REPO_DIR="bootstrap"
TMP_DIR=`mktemp -d`
RSA_FILE="rsa_2048.aes-256-cbc.enc"

# download the necessary parts
githubget ssh "sshup.sh"
githubget ssh "$RSA_FILE"
githubget bin "crypt"
chmod a+x "$TMP_DIR/sshup.sh"
chmod a+x "$TMP_DIR/crypt"

# set the ssh identity as my main user
PATH="$TMP_DIR:$PATH" $TMP_DIR/sshup.sh "$TMP_DIR/$RSA_FILE"

# clean up
rm -rf $TMP_DIR

# clone the bootstrap repo
if [ -d $REPO_DIR ]; then
    (cd $REPO_DIR; git fetch; git merge origin/master)
else
    git clone git@github.com:scyptnex/bootstrap.git $REPO_DIR
fi

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

