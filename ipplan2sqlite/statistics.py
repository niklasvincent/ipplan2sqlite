def print_all(c):
	# Number of nodes?
	c.execute('SELECT COUNT(*) FROM node')
	nbr_of_nodes = c.fetchone()[0]
	
	# Number of hosts?
	c.execute('SELECT COUNT(*) FROM host')
	nbr_of_hosts = c.fetchone()[0]
	
	# Number of networks?
	c.execute('SELECT COUNT(*) FROM network')
	nbr_of_networks= c.fetchone()[0]
	
	# Number of firewall rules?
	c.execute('SELECT COUNT(*) FROM firewall_rule')
	nbr_of_firewall_rules = c.fetchone()[0]
	
	print "Number of nodes:\t\t%d" % nbr_of_nodes
	print "Number of hosts:\t\t%d" % nbr_of_hosts
	print "Number of networks:\t\t%d" % nbr_of_networks
	print "Number of firewall rules:\t%d" % nbr_of_firewall_rules