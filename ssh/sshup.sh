#! /usr/bin/env bash

#-------------------------------------------------------------------------#
#                                sshup.sh                                 #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Mar-25                                                       #
#                                                                         #
# inserts the current ssh information into your .ssh directory, creating  #
# backups as needed                                                       #
#-------------------------------------------------------------------------#

set -e
set -u

SSH_DIR="$HOME/.ssh"
SSH_PRIV="$SSH_DIR/id_rsa"
SSH_PUBL="$SSH_DIR/id_rsa.pub"
CRYPTF="$1"
DECRYP=`mktemp`

crypt -f -o $DECRYP $CRYPTF

if [ -d "$SSH_DIR" ]; then
    [ -f "$SSH_PRIV" ] && mv "$SSH_PRIV" "$(mktemp $SSH_PRIV.backup.XXXX)"
    [ -f "$SSH_PUBL" ] && mv "$SSH_PUBL" "$(mktemp $SSH_PUBL.backup.XXXX)"
else
    mkdir -p "$SSH_DIR"
fi

head -n 1 $DECRYP > "$SSH_PUBL"
tail -n +2 $DECRYP > "$SSH_PRIV"
rm $DECRYP
