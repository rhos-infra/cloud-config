#!/bin/bash
args=("$@")

input="${args[0]}"
while IFS= read -r line
do
  if [[ "$line" == *"name: ${args[1]}"* ]]; then
    rolefound=1
  fi
  if [[ "$line" == *"vif"* && $rolefound ]]; then
    viffound=1
  fi
  if [[ "$line" == *"- network:"* && $viffound ]]; then
    networkfound=1
  fi
  if [[ "$line" != *"- network:"* && $networkfound ]]; then
    lastnetworkfound=1
  fi
  if [[ $lastnetworkfound ]] && ! [[ $updatemade ]]; then
    echo "  instances:"
    echo "  - hostname: ${args[2]}"
    echo "    name: ${args[3]}"
    echo "    provisioned: false"
    updatemade=1
  fi
  echo "$line"
done < $input

