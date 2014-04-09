#!/usr/bin/env python

from math import pow, ceil, log
from sys import argv


def min_pow2(x):                            # how many bits do we need to borrow
    z = log(x,2)                            # to cover number of hosts
    if int(z) != z:                         # in math language:
        z = ceil(z)                         # to which integer power do
    return int(z)                           # we need to raise 2 to get the number that is ge "x"


def getmask(cidr):                          # ex. 24 -> 255.255.255.0
    arr = [0 for i in range(4)]             # creating list of four 0s
    y = int(cidr / 8)                       # how many octets of 255
    if y > 0:                               # if mask < 8
        for z in range(y):
            arr[z] = 255
        arr[z + 1] = int(256 - pow(2, 8 - (cidr - 8 * y)))
    else:
        arr[0] = 256 - pow(2, 8-cidr)
    return arr


def getnet(ipaddr,nmask):                       # Get network address from ip and mask
    net = [0 for i in range(4)]
    for i in range(4):
        net[i]=int(ipaddr[i]) & int(nmask[i])   # octet and mask
    return net


def getfirst(ipaddr):                           # Get first usable address from ip and mask
    addr = ipaddr[:]
    addr[3] = int(addr[3]) + 1
    return addr


def getlast(ipaddr):                            # Get last usable address from ip and mask
    addr = ipaddr[:]                            # list is mutable, not to change the global value
    global ip, mask
    addr = getbcast(ip,mask)
    addr[3] -= 1
    return addr


def getbcast(ipaddr,nmask):                     # Get broadcast address from ip and mask
    net = [0 for i in range(4)]
    for i in range(4):
        net[i]=int(ipaddr[i]) | 255-int(nmask[i])    # octet or wildcard mask
    return net


def getnextaddr(ipaddr,nmask):
    ipaddr = getbcast(ipaddr,nmask)
    for i in range (4):
        if ipaddr[3-i] == 255:
            ipaddr [3-i] = 0
            if ipaddr[3-i-1] != 255:
                ipaddr[3-i-1] += 1
                break
        else:
            ipaddr[3-i] += 1
            break
    return ipaddr


def norm (ipaddr):
    addr = ipaddr[:]
    for i in range(len(addr)):
        addr[i] = str(addr[i])
    return ".".join(addr)


def vlsm(ipaddr,hosts):
    global cidr, need, allc
    bits = 0

    for x in range(len(hosts)):
        bits = min_pow2(hosts[x]+2)
        ipaddr = getnet(ipaddr,getmask(int(32-bits)))

        print "SUBNET: %d NEEDED: %4d (%3d %% of) ALLOCATED %4d ADDRESS: %15s MASK: %d (%15s)" % \
        (x+1,\
        hosts[x],\
        (hosts[x]*100)/(int(pow(2, bits))-2),\
        int(pow(2, bits))-2,\
        norm(ipaddr),\
        32-bits,\
        norm(getmask(int(32-bits))))

        need += hosts[x]
        allc += int(pow(2, bits))-2
        ipaddr = getnextaddr(ipaddr,getmask(int(32-bits)))

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
        # Example input ---> 192.168.1.0/24 2 8 22 54
        #
        # network  = 192.168.1.0
        # netmask  = 255.255.255.0
        # nethosts = 54, 22, 8, 2
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

ip   = argv[1].split("/")[0].split(".")             # 192.168.1.0/24 2 8 22 54  -> list of str ['192','168','1','0']
cidr = argv[1].split("/")[1]                        # 192.168.1.0/24 2 8 22 54  -> str 24
arg = [0 for i in range(len(argv[2:]))]             #                2 8 22 54  -> list of str ['2','8','22','54']
mask = getmask(int(cidr))                           #                       24  -> list of int [255,255,255,0]

for x in range(len(ip)):                            # list of str ['192','168','1','0'] ->
    ip[x] = int(ip[x])                              # list of int [192,168,1,0]

for x in range(len(argv[2:])):                      # list of str ['2','8','22','54'] ->
    arg[x] = int(argv[x+2])                         # list of int [2,8,22,54]

arg = sorted(arg, reverse=True)                     # sort (descending) list [2,8,22,54] -> [54,22,8,1]

need=0
allc=0

print
vlsm(getnet(ip,mask),arg)
print

print "STATISTICS"
print "=========="
print "Major Network: %s" % (argv[1])
print "Available IP addresses in major network: %d" % (pow(2,32-int(cidr))-2)
print "Number of IP addresses needed: ", need
print "Available IP addresses in allocated subnets: ", allc
print "About %d%% of available major network address space is used" % (((allc+(len(arg)*2))*100)/(pow(2,32-int(cidr))-2))
print "About %d%% of subnetted network address space is used" % (need*100/allc)
print