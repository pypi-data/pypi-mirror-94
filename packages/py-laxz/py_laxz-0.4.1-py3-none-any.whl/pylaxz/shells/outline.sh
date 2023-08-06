#! /bin/env bash

HEAD='\e[7;36m'
RESET='\e[m'
OUTPUT='\e[32m'
NL='\n'
ERROR='\e[3;31m'
WARN='\e[3;33m'

function has_curl() {
    dpkg-query -l curl >/dev/null 2>&1
    return $?
}

has_curl
if [[ $? -ne 0 ]]; then
    echo -e "${ERROR}'curl' is needed.${RESET}"
    exit 1
fi

read -p "API URL ? " API_URL

case "$1" in

--outline-get-lists)
    curl -H "Content-Type: application/json" --insecure $API_URL/access-keys
    ;;

*)
    echo -e "${ERROR}not an option.${RESET}"
    ;;
esac
