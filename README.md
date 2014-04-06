vlsm
====

Variable Length Subnet Mask

This module accepts the initial network/mask that needs to be sliced up and the set of arguments 
with the number of end hosts in each subnet.

The example of parameters that needs to be provided as follows:

python vlsm.py 192.168.1.0/24 13 22 101 8 8 5 2



jabbson@linux $ python vlsm.py 192.168.1.0/24 13 22 101 8 8 5 2

SUBNET: 0 NEEDED: 101 ALLOCATED 128 ADDRESS: 192.168.1.0    MASK: 25 ( 255.255.255.128 )
SUBNET: 1 NEEDED: 22 	ALLOCATED 32 	ADDRESS: 192.168.1.128 	MASK: 27 ( 255.255.255.224 )
SUBNET: 2 NEEDED: 13 	ALLOCATED 16 	ADDRESS: 192.168.1.160 	MASK: 28 ( 255.255.255.240 )
SUBNET: 3 NEEDED: 8 	ALLOCATED 16 	ADDRESS: 192.168.1.176 	MASK: 28 ( 255.255.255.240 )
SUBNET: 4 NEEDED: 8 	ALLOCATED 16 	ADDRESS: 192.168.1.192 	MASK: 28 ( 255.255.255.240 )
SUBNET: 5 NEEDED: 5 	ALLOCATED 8 	ADDRESS: 192.168.1.208 	MASK: 29 ( 255.255.255.248 )
SUBNET: 6 NEEDED: 2 	ALLOCATED 4 	ADDRESS: 192.168.1.216 	MASK: 30 ( 255.255.255.252 )

jabbson@linux $ 
