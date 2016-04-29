#! /usr/bin/env bash

#-------------------------------------------------------------------------#
#                              mkidentity.sh                              #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Apr-29                                                       #
#-------------------------------------------------------------------------#

set -eu

cat ~/.ssh/id_rsa.pub ~/.ssh/id_rsa <(gpg --export bootstrap) <(gpg --export-secret-key bootstrap) | gpg --symmetric --cipher-algo AES256 --armor --no-use-agent

