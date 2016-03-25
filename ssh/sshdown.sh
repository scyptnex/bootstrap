#! /usr/bin/env bash

#-------------------------------------------------------------------------#
#                               sshdown.sh                                #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Mar-25                                                       #
#                                                                         #
# Creates a new ssh identity (mainly for posterity)                       #
#-------------------------------------------------------------------------#

set -e
set -u

echo "Your email is $EMAIL"
TMPF="$(dirname $0)/tmpkey"
OUTP="$(dirname $0)/rsa_2048"
ssh-keygen -f $TMPF $@
cat ${TMPF}.pub ${TMPF} | sed "s/ [a-zA-Z0-9._-]*@[a-zA-Z0-9._-]*/ $EMAIL/" > $OUTP
crypt $OUTP
rm $TMPF ${TMPF}.pub $OUTP
