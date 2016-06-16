#! /usr/bin/env bash

#=========================================================================#
#                              fix_remote.sh                              #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Jun-16                                                       #
#                                                                         #
# overrides the remote for the current repository to be the SSH remote    #
#=========================================================================#

set -e
set -u

DIR=$(readlink -f `dirname $0`/.. )

(cd $DIR && git remote set-url origin git@github.com:scyptnex/bootstrap.git)

