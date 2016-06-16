#! /usr/bin/env bash

#============================================================================#
#                             create_identity.sh                             #
#                                                                            #
# Author: Nic H.                                                             #
# Date: 2016-Apr-29                                                          #
#============================================================================#

set -e
set -u

gpg --list-key $1 >&2

# hard coding the security like this is questionable
# on the other hand, defaulting to sha1 is no good...
cat ~/.ssh/id_rsa.pub ~/.ssh/id_rsa <(gpg --export $1) <(gpg --export-secret-key $1) |
    gpg --symmetric --s2k-cipher-algo AES256 --s2k-digest-algo SHA512 --s2k-mode 3 --s2k-count 65000000 --armor --no-use-agent

