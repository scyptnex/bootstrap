#! /usr/bin/env bash

#-------------------------------------------------------------------------#
#                             getidentity.sh                              #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Apr-29                                                       #
#-------------------------------------------------------------------------#

set -eu

ALL=`mktemp`
trap "rm $ALL" EXIT

gpg --no-use-agent > $ALL
LN=`grep -na "^\-*END RSA PRIVATE KEY\-*$" $ALL | head -n 1 | cut -d ":" -f 1`
head -n 1 $ALL > ~/.ssh/id_rsa.pub
head -n $LN $ALL | tail -n +2 > ~/.ssh/id_rsa
tail -n +$((LN + 1)) $ALL | gpg --import

# automatically imports trust level ultimate for the bootstrap key
gpg --list-key --fingerprint bootstrap | grep fingerprint | tail -1 | tr -d '[:space:]' | sed -e 's/^.*=//' -e 's/$/:6:\n/' | gpg --import-ownertrust

