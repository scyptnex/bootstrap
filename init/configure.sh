#! /usr/bin/env bash

#=========================================================================#
#                              configure.sh                               #
#                                                                         #
# Author: Nic H.                                                          #
# Date: 2016-Jun-16                                                       #
#                                                                         #
# Create the configurations (dotfiles) as needed                          #
#=========================================================================#

set -e
set -u

stow -Rv --dir=${HOME}/project/bootstrap/dotfiles/ --target=${HOME} --no-folding .
