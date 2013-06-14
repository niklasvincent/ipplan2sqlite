def create(conn):
	c = conn.cursor()
	
	# Node
	c.execute('''CREATE TABLE node(
	id INTEGER PRIMARY KEY AUTOINCREMENT)''')
	
	# Hosts
	c.execute('''CREATE TABLE host(
	node_id INTEGER, name TEXT, ipv4_addr INTEGER, ipv4_addr_txt TEXT, ipv6_addr_txt TEXT, network_id INTEGER, 
	FOREIGN KEY (node_id) REFERENCES node (id), FOREIGN KEY (network_id) REFERENCES network (id))''')
	
	# Networks
	c.execute('''CREATE TABLE network(
	node_id INTEGER, name TEXT, vlan INTEGER, terminator TEXT, ipv4_addr INTEGER, ipv4_addr_txt TEXT,
	ipv6_txt TEXT, ipv4_netmask INTEGER, ipv4_netmask_txt TEXT, ipv6_netmask_txt TEXT, ipv4_gateway INTEGER, 
	ipv4_gateway_txt TEXT, ipv6_gateway_txt TEXT, ipv4_netmask_dec INTEGER, ipv6_capable INTEGER,
	FOREIGN KEY (node_id) REFERENCES node (id))''')
	
	# Options
	c.execute('''CREATE TABLE option(
	id INTEGER PRIMARY KEY AUTOINCREMENT, node_id INTEGER, name TEXT, value TEXT,
	FOREIGN KEY (node_id) REFERENCES node (id))''')
	
	# Services
	c.execute('''CREATE TABLE service(
	id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, dst_ports TEXT, src_ports TEXT)''')
	
	# Flows
	c.execute('''CREATE TABLE flow(
	id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)''')
	
	# Firewall rules
	c.execute('''CREATE TABLE firewall_rule(
	id INTEGER PRIMARY KEY AUTOINCREMENT, from_node_id INTEGER, to_node_id INTEGER,
	service_id INTEGER, flow_id INTEGER, is_ipv4 BOOLEAN, is_ipv6 BOOLEAN,
	FOREIGN KEY (from_node_id) REFERENCES node (id), FOREIGN KEY (to_node_id) REFERENCES node (id),
	FOREIGN KEY (service_id) REFERENCES service (id), FOREIGN KEY (flow_id) REFERENCES flow (id))''')
	
	# Meta data
	c.execute('''CREATE TABLE meta_data(name TEXT, value TEXT)''')
	
	conn.commit()