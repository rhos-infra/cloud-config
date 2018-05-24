---
config:
    plugin_type: install
subparsers:
    cloud-config:
        description: Collection of overcloud configuration tasks
        include_groups: ["Ansible options", "Inventory", "Common options", "Answers file"]
        groups:
            - title: Tasks Control
              options:
                  tasks:
                      type: ListOfFileNames
                      help: |
                          Provide a option to run one or more tasks to the cloud. If you run two or more tasks
                          at once, you need to separate them with commas
                          Example: infrared cloud-config --task task1,task3,task2
                          Note: Tasks represent playbooks, which are stored in the 'lookup_dir' folder in plugin
                          directory. Task run in the same order as they are provided.
                      lookup_dir: 'post_tasks'
                      required: yes

            - title: OSP version parameters
              options:
                  mirror:
                      type: Value
                      help: |
                          Enable usage of specified mirror (for rpm, pip etc) [brq,qeos,tlv - or hostname].
                          (Specified mirror needs to proxy multiple rpm source hosts and pypi packages.)

                  version:
                      type: Value
                      help: |
                          The product version (product == director)
                          Numbers are for OSP releases
                          Names are for RDO releases
                          Note: It is not mandatory, if not provided plugin will use value from automatic version discovery
                      choices:
                        - "7"
                        - "8"
                        - "9"
                        - "10"
                        - "11"
                        - "12"
                        - "13"
                        - kilo
                        - liberty
                        - mitaka
                        - newton
                        - ocata
                        - pike
                        - queens
                  build:
                      help: |
                          String represents a timestamp of the OSP puddle.
                          Note: for versions 6 < OSPd < 10 to specify director
                          version use '--director-build' flag.
                          (for the given product core version).
                          Supports any rhos-release labels.
                          RDO supported labels: master-tripleo-ci
                          Examples: "passed_phase1", "2016-08-11.1", "Y1", "Z3", "GA"
                      type: Value

                  director-build:
                      help: |
                          String represents a timestamp of the OSP director puddle
                          (for the given product core version). Only applies for
                          6 < OSPd < 10, and could be used with '--build' flag.
                          Note: for versions >= 10 only the --build flag should be used to
                          specify a puddle.
                          Supports any rhos-release labels.
                          Examples: "passed_phase1", "2016-08-11.1", "Y1", "Z3", "GA"
                          If missing, will equal to "latest".
                      type: Value

                  buildmods:
                      type: Value
                      help: |
                          List of flags for rhos-release module.
                          Currently works with
                          pin - pin puddle (dereference 'latest' links to prevent content from changing)
                          flea - enable flea repos
                          unstable - this will enable brew repos or poodles (in old releases)
                          cdn - use internal mirrors of the CDN repos. (internal use)
                          none - use none of those flags
                      default: pin

                  enable-testing-repos:
                      type: Value
                      help: |
                          Let you the option to enable testing/pending repos with rhos-release. Multiple values have to be coma separated.
                          Examples: --enable-testing-repos rhel,extras,ceph or --enable-testing-repos all


            - title: Common parameters
              options:
                  overcloud-stack:
                      type: Value
                      help: The overcloud stack name
                      default: overcloud

                  splitstack:
                      type: Bool
                      default: no
                      help: |
                        If customer has already provisioned nodes for an overcloud splitstack should be used to utilize these
                        nodes.(https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/11/html/director_installation_and_usage/chap-configuring_basic_overcloud_requirements_on_pre_provisioned_nodes)

            - title: TripleO User
              options:
                  user-name:
                      type: Value
                      help: The installation user name. Will be generated if missing
                      default: stack

                  user-password:
                      type: Value
                      help: The installation user password
                      default: stack

            - title: Service Discovery
              options:
                  resync:
                      type: Bool
                      help: |
                          Whether we need to resync services.
                          Used with service discovery.
                      default: False

            - title: External Network
              options:
                  deployment-files:
                      type: Value
                      help: |
                          Name of folder in cloud's user on undercloud, which containing the templates of
                          the overcloud deployment.

                  network-protocol:
                      type: Value
                      help: The overcloud network backend.
                      default: ipv4
                      choices:
                          - ipv4
                          - ipv6

                  public-net-name:
                      type: Value
                      help: |
                          Specifies the name of the public network.
                          NOTE: If not provided it will use the default one for the OSP version

                  public-subnet:
                      type: VarFile
                      help: |
                          Subnet detail for "public" external network on the overcloud as post-install.
                          (CIDR, Allocation Pool, Gateway)
                          __LISTYAMLS__
                      default: default_subnet

                  external-vlan:
                      type: Value
                      help: |
                         An Optional external VLAN ID of the external network (Not to be confused with the Public API network)

            - title: Scale down nodes
              options:
                  node-name:
                      type: Value
                      help: |
                        Name of the node to remove

            - title: Scale up nodes
              options:
                 scale-nodes:
                      type: ListValue
                      help: |
                            List of compute nodes to be added.
                            Example: compute-3,compute-4,compute-5
                            NOTE: When you scale up splitstack deployment, you can use all "OSP version parameters" to
                            control rhos_release options.

            - title: Ironic Configuration
              options:
                  vbmc-username:
                      type: Value
                      default: admin
                      help: |
                        VBMC username (Necessary when Ironic's driver is 'pxe_ipmitool' - OSP >= 11)
                  vbmc-password:
                      type: Value
                      default: password
                      help: |
                        VBMC password (Necessary when Ironic's driver is 'pxe_ipmitool' - OSP >= 11)
                  resource-class-enabled:
                      type: Bool
                      default: True
                      help: |
                          Scheduling based on resource classes, a Compute service flavor is able to use the
                          node’s resource_class field (available starting with Bare Metal API version 1.21)
                          for scheduling, instead of the CPU, RAM, and disk properties defined in the flavor.
                          A flavor can request exactly one instance of a bare metal resource class.
                          (https://docs.openstack.org/ironic/latest/install/configure-nova-flavors.html#scheduling-based-on-resource-classes)
                          Scheduling based on resource classes is enabled by default if OSP>=12. This option
                          allows to disable it.
                          Example: --resource-class-enabled False
                  resource-class-override:
                      type: NestedList
                      action: append
                      help: |
                          This option allows to create custom resource class and tie it to flavor and instances.
                          The 'node' field supports 'controller' or 'controller-0' patterns.
                          Example:
                              --resource-class-override name=baremetal-ctr,flavor=controller,node=controller
                              --resource-class-override name=baremetal-cmp,flavor=compute,node=compute-0
                              --resource-class-override name=baremetal-other,flavor=compute,node=swift-0:baremetal
            - title: Workload Launch
              options:
                  workload-image-url:
                      type: Value
                      default: 'http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img'
                      help: |
                        Image source URL that should be used for uploading the workload Glance image
                  workload-memory:
                      type: Value
                      default: '512'
                      help: |
                        Amount of memory allocated to test workload flavor
                  workload-vcpu:
                      type: Value
                      default: '1'
                      help: |
                        Amount of vcpus allocated to test workload flavor
                  workload-disk:
                      type: Value
                      default: '5'
                      help: |
                        Disk size allocated to test workload flavor
                  workload-index:
                      type: Value
                      default: '1'
                      help: |
                        Number of workload objects to be created

            - title: Deployment Description
              options:
                  ntp-server:
                      type: Value
                      help: Ntp server name (or IP) to use.
                      default: clock.redhat.com
                  hybrid:
                      type: Bool
                      help: Specifies whether deploying a hybrid environment.
                      default: no
            - title: Storage
              options:
                  storage-external:
                      type: Bool
                      help: Whether to use an external storage rather than setting it up with the director
                      default: no

                  storage-backend:
                      type: Value
                      choices:
                          - ceph
                          - swift
                          - netapp-iscsi
                          - netapp-nfs
                          - lvm
                      help: |
                        The storage that we would like to use.
                        If not supplied, Infrared will try to discover storage nodes and select appropriate backed.
                        The 'lvm' value will be used when storage nodes were not found.
                        NOTE: when not using external storage, this will set the default for "--storage-nodes" to 1.
            - title: Control Node Placement
              options:
                  specific-node-ids:
                      type: Bool
                      default: no
                      help: |
                          Default tagging behaviour is to set properties/capabilities profile, which is based on the
                          node_type for all nodes from this type. If this value is set to true/yes, default behaviour
                          will be overwritten and profile will be removed, node id will be added to properties/capabilities
                          and scheduler hints will be generated.
                          Examples of node IDs include controller-0, controller-1, compute-0, compute-1, and so forth.
