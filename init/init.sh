#! /usr/bin/env bash

#=========================================================================#
#                                 init.sh                                 #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Jun-16                                                       #
#                                                                         #
# main initialisation script, basically it just calls the relevant sub-   #
# scripts                                                                 #
#=========================================================================#

set -e
set -u

DIR=$(readlink -f `dirname $0`)

$DIR/load_identity.sh $DIR/../identity/2016-06-16.asc
$DIR/fix_remote.sh
$DIR/configure.sh

