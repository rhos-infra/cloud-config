#!/bin/bash
#
# This script updates baremetal_deployment.yaml by inserting provisioned: false
# for the requested instance. It handles formats of baremetal_deployment.yaml
# where instances already exist and formats where no instances exist yet.
#
# inputs:
#
# arg[0] - The path to the baremetal_deployment.yaml being updated
# arg[1] - The role name being updated e.g. Compute
# arg[2] - The hostname of the node being deleted e.g. compute-0
# arg[3] - The nodename of the node being deleted e.g. compute-0
#
# Example invocation:
#
# ./insert_instance.sh home/stack/virt/network/baremetal_deployment_preinstance.yaml
# Compute compute-0 compute-0 > /home/stack/virt/network/baremetal_deployment.yaml

args=("$@")

input="${args[0]}"

# Determine if node name exists in baremetal_deployment.yaml
while IFS= read -r line
do
  if [[ "$line" == *" name: ${args[3]}"* ]]; then
    instanceexists=1
  fi
done < $input

# Update baremetal_deployment.yaml when it contains node name
if [[ $instanceexists ]]; then
    while IFS= read -r line
    do
      echo "$line"
      if [[ "$line" == *" name: ${args[3]}"* ]]; then
        nodenamefound=1
      fi
      if [[ $nodenamefound ]] && ! [[ $updatemade ]]; then
        echo "    provisioned: false"
        updatemade=1
      fi
    done < $input
fi

# Exit script if baremetal_deployment.yaml successfully updated
if [[ "$updatemade" == "1" ]]; then
    exit 0
fi

# Update baremetal_deployment.yaml when it does not contain node name
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

# Exit script with success or fail depending on whether requested update was made
if [[ "$updatemade" == "1" ]]; then
    exit 0
else
    exit 1
fi
