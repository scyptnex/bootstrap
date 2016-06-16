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
which gpg >/dev/null 2>/dev/null || (echo "Install gpg" >&2 && exit 1)

# check we arent overwriting an existing identity (i.e. prompt the user to save their current one)
(gpg -k bootstrap >/dev/null 2>/dev/null || gpg -K bootstrap >/dev/null 2>/dev/null) && (echo "gpg key 'bootstrap' already exists" >&2 && exit 1)
[ ! -f ~/.ssh/id_rsa ] || (echo "id_rsa exists" >&2 && exit 1)
[ ! -f ~/.ssh/id_rsa.pub ] || (echo "id_rsa.pub exists" >&2 && exit 1)

#important variables
REPO_DIR="bootstrap"
TMP_DIR=`mktemp -d`

# download the necessary parts
githubget identity "identity.asc"
githubget identity "getidentity.sh"
chmod a+x "$TMP_DIR/getidentity.sh"

# set the ssh/gpg identity as my main user
$TMP_DIR/getidentity.sh < "$TMP_DIR/identity.asc"

# clean up
rm -rf $TMP_DIR

# clone the bootstrap repo
if [ -d $REPO_DIR ]; then
    (cd $REPO_DIR; git fetch; git merge origin/master)
else
    git clone git@github.com:scyptnex/bootstrap.git $REPO_DIR
fi

$REPO_DIR/init/configure.sh

