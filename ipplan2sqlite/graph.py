# -*- coding: utf-8 -*-
"""
pydot example 2
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
import pydot, sqlite3, sys, colorsys

try:
	conn = sqlite3.connect("ipplan.db")
	c = conn.cursor()
	
except sqlite.Error, e:
	print "Error %s:" % e.args[0]
	sys.exit(1)

local_networks = ['DREAMHACK', 'RFC_10', 'RFC_172', 'RFC_192']

graph = pydot.Dot(graph_type='digraph', splines='true', concentrate='true', pack='true', center='true', dpi='600')

# Generate colors
c.execute('''SELECT COUNT(*) FROM service;''')
N = int(c.fetchone()[0])
hexcolors = []
HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
for RGB in RGB_tuples:
	hexcolors.append('#%02x%02x%02x' % (RGB[0] * 255, RGB[1] * 255, RGB[2] * 255))

# Color code services
services = {}
i = 0
c.execute('''SELECT id, name FROM service;''')
for service in c.fetchall():
	services[str(service[1])] = { 'id' : str(service[0]), 'color' : hexcolors[i] }
	i = i + 1

nodes = {}
c.execute('''SELECT name, node_id FROM host''')
for host in c.fetchall():
	nodes[int(host[1])] = str(host[0])
c.execute('''SELECT name, node_id FROM network''')
for network in c.fetchall():
	nodes[int(network[1])] = str(network[0])

if len(sys.argv) == 1:
	c.execute('''SELECT f.from_node_id, f.to_node_id, f.is_ipv4, f.is_ipv6, fl.name, s.name, s.dst_ports 
					FROM service s, firewall_rule f, flow fl WHERE s.id = f.service_id AND fl.id = f.flow_id;''')
else:
	c.execute('''SELECT f.from_node_id, f.to_node_id, f.is_ipv4, f.is_ipv6, fl.name, s.name, s.dst_ports 
					FROM service s, firewall_rule f, flow fl WHERE s.id = f.service_id AND fl.id = f.flow_id AND s.name = ?;''', (sys.argv[1],))

for rule in c.fetchall():
	if nodes[rule[0]] in local_networks:
		from_node = 'DREAHACK/RFC 1918'
	else:
		from_node = nodes[rule[0]]
	if from_node == "ANY":
		from_node = "INTERNET"
	edge = pydot.Edge(pydot.Node(from_node, fontsize="16.0", shape="box", fillcolor="green", color="#FF0000", style='bold', href='javascript:alert("HEJ");'), pydot.Node(nodes[rule[1]], fontsize="16.0", style="filled", fillcolor="green"), label=rule[5], labelfontcolor="#009933", fontsize="10.0", color=services[rule[5]]['color'])
	graph.add_edge(edge)

graph.write_svg('firewall.svg', prog='fdp')
graph.write_png('firewall.png')


conn.close()