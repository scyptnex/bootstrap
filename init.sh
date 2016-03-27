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
TMP_DIR=`mktemp -d`
RSA_FILE="rsa_2048.aes-256-cbc.enc"
githubget ssh "sshup.sh"
githubget ssh "$RSA_FILE"
githubget bin "crypt"
chmod a+x "$TMP_DIR/sshup.sh"
chmod a+x "$TMP_DIR/crypt"
PATH="$PATH:$TMP_DIR" $TMP_DIR/sshup.sh "$TMP_DIR/$RSA_FILE"
rm -rf $TMP_DIR
git clone git@github.com:scyptnex/bootstrap.git

