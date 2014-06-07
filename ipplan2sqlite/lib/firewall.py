import re
import json

def add_services(services, c):
    for service in services:
        row = [str(service['service']), str(service['description']), str(service['destport']), str(service['sourceport'])]
        c.execute('INSERT INTO service VALUES (NULL, ?, ?, ?, ?)', row)

def add_flows(flows, c):
    for flow in flows:
        row = [str(flow['name']), str(flow['description'])]
        c.execute('INSERT INTO flow VALUES (NULL, ?, ?)', row)
    c.execute('INSERT INTO flow VALUES (NULL, ?, ?)', ['normal', 'normal flow'])

def build(c):
    client_server(c)
    local(c)
    public(c)
    world(c)
    return

def client_server(c):
    # Select all servers
    c.execute('SELECT node_id, value FROM option WHERE name = ?', ('s', ))
    servers = c.fetchall()

    for server in servers:
        to_node_id              = int(server[0])

        service = parse_service(c, server[1])

        # Select all clients
        c.execute('SELECT node_id FROM option WHERE name = ? AND value = ?', ('c', service['full_name']))
        clients = c.fetchall()

        for client in clients:
            from_node_id = int(client[0])
            row = [from_node_id, to_node_id, service['service_id'], service['flow_id'], service['is_ipv4'], service['is_ipv6']]
            c.execute('INSERT INTO firewall_rule VALUES (NULL, ?, ?, ?, ?, ?, ?)', row)
    return

def local(c):
    # Select all servers providing services to their VLAN
    c.execute('SELECT node_id, value FROM option WHERE name = ?', ('l', ))
    servers = c.fetchall()
    for server in servers:
        to_node_id = int(server[0])

        # What service?
        service = parse_service(c, server[1])

        # Which VLAN is this server on?
        c.execute('SELECT network_id FROM host WHERE node_id = ?', (to_node_id,))
        from_node_id = int(c.fetchone()[0])
        row = [from_node_id, to_node_id, service['service_id'], service['flow_id'], service['is_ipv4'], service['is_ipv6']]
        c.execute('INSERT INTO firewall_rule VALUES (NULL, ?, ?, ?, ?, ?, ?)', row)
    return

def public(c):
    # List public networks
    network_node_ids = {}
    for network in ['DREAMHACK', 'RFC_10', 'RFC_172', 'RFC_192']:
        network_node_ids[network] = get_network_node_id(c, network)

    # Select all servers providing services to their VLAN
    c.execute('SELECT node_id, value FROM option WHERE name = ?', ('p', ))
    servers = c.fetchall()
    for server in servers:
        to_node_id = int(server[0])

        # What service?
        service = parse_service(c, server[1])

        for network in network_node_ids:
            from_node_id = network_node_ids[network]
            row = [from_node_id, to_node_id, service['service_id'], service['flow_id'], service['is_ipv4'], service['is_ipv6']]
            c.execute('INSERT INTO firewall_rule VALUES (NULL, ?, ?, ?, ?, ?, ?)', row)
    return

def world(c):
    # Reference for internet
    from_node_id = get_network_node_id(c, "ANY")

    # Select all servers providing services to their VLAN
    c.execute('SELECT node_id, value FROM option WHERE name = ?', ('w', ))
    servers = c.fetchall()
    for server in servers:
        to_node_id = int(server[0])

        # What service?
        service = parse_service(c, server[1])
        row = [from_node_id, to_node_id, service['service_id'], service['flow_id'], service['is_ipv4'], service['is_ipv6']]
        c.execute('INSERT INTO firewall_rule VALUES (NULL, ?, ?, ?, ?, ?, ?)', row)
    return

def parse_service(c, service):
    service_version = str(re.compile(r'[^\d.]+').sub('', service))
    is_ipv4             = 0
    is_ipv6                 = 0
    if "4" in service_version:
        is_ipv4 = 1
    if "6" in service_version:
        is_ipv6 = 1
    service_name    = service.replace(service_version, '')

    # Flow?
    if "-" in service_name:
        flow_name               = service_name.split('-')[0]
        service_name    = service_name.split('-')[-1]
    else:
        flow_name = 'normal'
    flow_id                         = get_flow_id(c, flow_name)

    # Service?
    service_id      = get_service_id(c, service_name)

    return {"full_name" : service, "service_id" : service_id, "flow_id" : flow_id, "is_ipv4" : is_ipv4, "is_ipv6" : is_ipv6}

def get_flow_id(c, flow_name):
    c.execute('SELECT id FROM flow WHERE name = ?', (flow_name, ))
    return int(c.fetchone()[0])

def get_service_id(c, service_name):
    c.execute('SELECT id FROM service WHERE name = ?', (service_name, ))
    return int(c.fetchone()[0])

def get_network_node_id(c, network_name):
    c.execute('SELECT node_id FROM network WHERE name = ?', (network_name,))
    return c.fetchone()[0]
