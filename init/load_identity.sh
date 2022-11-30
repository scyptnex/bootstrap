#! /usr/bin/env bash

#-------------------------------------------------------------------------#
#                            load_identity.sh                             #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Apr-29                                                       #
#-------------------------------------------------------------------------#

set -e
set -u

ALL=`mktemp`
trap "rm -f $ALL" EXIT

rm $ALL && gpg --no-use-agent -o $ALL $1
LN=`grep -na "^\-*END RSA PRIVATE KEY\-*$" $ALL | head -n 1 | cut -d ":" -f 1`

[ -d ~/.ssh ] || mkdir ~/.ssh
[ -f ~/.ssh/id_rsa ] && mv ~/.ssh/{,BACKUP_}id_rsa
[ -f ~/.ssh/id_rsa.pub ] && mv ~/.ssh/{,BACKUP_}id_rsa.pub

head -n 1 $ALL > ~/.ssh/id_rsa.pub
head -n $LN $ALL | tail -n +2 > ~/.ssh/id_rsa
tail -n +$((LN + 1)) $ALL | gpg --batch --import

# automatically imports trust level ultimate for the bootstrap key
#KEY=`tail -n +$((LN + 1)) "$ALL" | gpg --list-packets 2>/dev/null | grep "^:user" | sed -e 's/^[^"]*"//' -e 's/"$//' | sort -u`
#gpg --list-key --fingerprint "$KEY" | grep fingerprint | tail -1 | tr -d '[:space:]' | sed -e 's/^.*=//' -e 's/$/:6:\n/' | gpg --import-ownertrust 2>&1

cat << EOF

You must now setup the trust for this key:

gpg --edit-key bootstrap
> trust
> 5
> y
> quit

EOF
