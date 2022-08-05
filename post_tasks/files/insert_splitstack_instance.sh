#!/bin/bash
args=("$@")

input="${args[0]}"
while IFS= read -r line
do
  if [[ "$line" == *"name: ${args[1]}"* ]]; then
    rolefound=1
  fi
  if [[ "$line" == *"instances"* && $rolefound ]]; then
    instancesfound=1
  fi
  echo "$line"
  if [[ $instancesfound ]] && ! [[ $updatemade ]]; then
    echo "  - hostname: ${args[2]}"
    echo "    managed: false"
    echo "    networks:"
    echo "      - network: ctlplane"
    echo "        fixed_ip: ${args[3]}"
    echo "      - network: storage"
    echo "      - network: internal_api"
    echo "      - network: tenant"
    echo "      - network: external"
    updatemade=1
  fi
done < $input
if [[ "$updatemade" == "1" ]]; then
    exit 0
else
    exit 1
fi
