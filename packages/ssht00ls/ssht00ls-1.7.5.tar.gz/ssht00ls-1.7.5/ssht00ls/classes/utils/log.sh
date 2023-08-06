# colors.
purple="\033[95m"
cyan="\033[96m"
orange='\033[33m'
blue="\033[94m"
green="\033[92m"
yellow="\033[93m"
grey="\033[90m"
red="\033[91m"
end="\033[0m"

#! /bin/sh
# logs the argument messages & kills the connection
# usage: ../message_kill.sh "You are not authorized" "Closing the connection"
for var in "$@"
do
    echo "$var"
done
exit 1