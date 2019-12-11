#!/bin/bash

user="some-user"
pass="some-pass"
send_to="$1"
subject=$(echo "$2"| sed "s/\"/'/g")
lang="$3"

text=$(python -c "import urllib; print(urllib.quote(\"$subject\"));")

curl -u "$user:$pass" $send_to/$lang/$text
