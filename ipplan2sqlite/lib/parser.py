import ipcalc
import re
import socket
import struct
import sys
from binascii import hexlify

MODULE = sys.modules[ __name__ ]

SYNTAX = {"^#@" : "master_network", "^#\$" : "host", "^[A-Z]" : "network" }

def master_network(l, c, r):
    if r is not None:
        node_id                         = node(c)
        name                            = 'DREAMHACK'
        vlan                            = 0
        terminator                      = ''

        # IPv4
        ipv4                            = r[2]
        net_ipv4                        = ipcalc.Network(ipv4)
        ipv4_gateway            = net_ipv4[1]
        ipv4_netmask            = str(net_ipv4.netmask())
        ipv4_netmask_dec        = int(str(l[2]).split("/")[1])

        # IPv6
        ipv6                            = l[2]
        last_digits                     = int(str(ipv4_gateway).split('.')[-1])
        ipv6_netmask            = 64
        ipv6_gateway            = "2001:67c:24d8:::%d" % last_digits

        row = [node_id, name, vlan, terminator, ip2long(ipv4, 4),
        str(ipv4), str(ipv6), ip2long(ipv4_netmask, 4), str(ipv4_netmask),
        str(ipv6_netmask), ip2long(ipv4_gateway, 4), str(ipv4_gateway),
        str(ipv6_gateway), int(ipv4_netmask_dec), 1]

        c.execute('INSERT INTO network VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
    else:
        return l
    return

def host(l, c, vlan):
    node_id = node(c)
    c.execute('SELECT node_id FROM network WHERE vlan = ?', (vlan, ))
    network_id = int(c.fetchone()[0])

    name                    = l[1]
    ipv4_addr               = l[2]
    last_digits             = int(str(ipv4_addr).split('.')[-1])
    ipv6_addr               = "2001:67c:24d8:%d::%d" % (vlan, last_digits)

    row = [node_id, name, ip2long(ipv4_addr, 4), ipv4_addr, ipv6_addr, network_id]
    c.execute('INSERT INTO host VALUES (?,?,?,?,?,?)', row)

    options(c, node_id, l[3])

    return

def network(l, c, r):
    node_id         = node(c)
    name            = l[0]
    vlan            = int(l[3])
    terminator      = l[1]

    # IPv4
    ipv4                            = l[2]
    net_ipv4                        = ipcalc.Network(l[2])
    ipv4_gateway            = net_ipv4[1]
    ipv4_netmask            = str(net_ipv4.netmask())
    ipv4_netmask_dec        = int(str(l[2]).split("/")[1])

    # IPv6
    last_digits                     = int(str(ipv4_gateway).split('.')[-1])
    ipv6                            = "2001:67c:24d8:%d::/64" % vlan
    ipv6_netmask            = 64
    ipv6_gateway            = "2001:67c:24d8:%d::%d" % (vlan, last_digits)

    row = [node_id, name, vlan, terminator, ip2long(ipv4, 4),
    str(ipv4), str(ipv6), ip2long(ipv4_netmask, 4), str(ipv4_netmask),
    str(ipv6_netmask), ip2long(ipv4_gateway, 4), str(ipv4_gateway),
    str(ipv6_gateway), int(ipv4_netmask_dec), 1]
    c.execute('INSERT INTO network VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)

    options(c, node_id, l[4])

    return int(vlan)

def options(c, node_id, options):
    for option in options.split(';'):
        option = option.split("=")
        name = option[0]
        if len(option) == 2:
            values = option[1].split(',')
            for value in values:
                row = [node_id, name, value]
                c.execute('INSERT INTO option VALUES(NULL, ?, ?, ?)', row)
        else:
            row = [node_id, name, 1]
            c.execute('INSERT INTO option VALUES(NULL, ?, ?, ?)', row)


def node(c):
    c.execute('INSERT INTO node VALUES (NULL)')
    c.execute('SELECT last_insert_rowid() as id')
    return int(c.fetchone()[0])

def ip2long(ip, version):
    ip = str(ip).split("/")[0]
    if version == 4:
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]
    else:
        return int(hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)

def parser_func(l):
    for exp in SYNTAX:
        if re.match( exp, l[0] ):
            return SYNTAX[exp]
    return None

def parse(lines, c):
    vlan = None
    for line in lines:
        if isinstance( line, str ):
            line = line.strip().split()
        if len( line ) == 0:
            continue
        func = parser_func( line )
        if func:
            parse_using = getattr( MODULE, func, vlan )
            result = parse_using( line, c, vlan )
            vlan = result if result is not None else vlan
