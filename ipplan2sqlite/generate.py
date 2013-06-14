#!/usr/bin/python
import sqlite3, os, sys, re, json

SYNTAX = {"^#@" : "master_network", "^#\$" : "host", "^[A-Z]" : "network" }

# Check arguments
if len(sys.argv) < 4:
	print "Usage: %s ipplan services flows" % sys.argv[0]
	sys.exit(1)

# Create fresh database file
DB_FILE = "ipplan.db"
if os.path.isfile(DB_FILE):
	os.unlink(DB_FILE)
	
try:
	conn = sqlite3.connect(DB_FILE)
	c = conn.cursor()
	
	c.execute('SELECT SQLITE_VERSION()')
	data = c.fetchone()
	print "SQLite version: %s" % data
	
except lite.Error, e:
	print "Error %s:" % e.args[0]
	sys.exit(1)

# Create tables
import tables
tables.create(conn)

# Read the ipplan file
ipplan_file = sys.argv[1]
if not os.path.isfile(ipplan_file):
	print "Could not open file %s" % ipplan_file
	sys.exit(2)

# Parse ipplan
import parser
lines = [line.strip().split() for line in open(ipplan_file)]

vlan = None
for l in lines:
	if len(l) == 0:
		continue
	for exp in SYNTAX:
		if re.match(exp, l[0]):
			parse_using = getattr(parser, SYNTAX[exp], vlan)
			result = parse_using(l, c, vlan)
			if not result is None:
				vlan = result
				
# Add custom networks
import networks
networks.add_all(c)

# Read the services file
services_file = sys.argv[2]
if not os.path.isfile(services_file):
	print "Could not open file %s" % services_file
	sys.exit(3)
services = json.loads(open(services_file, 'r').read())

# Add services to database
for service in services:
	row = [str(service['service']), str(service['description']), str(service['destport']), str(service['sourceport'])]
	c.execute('INSERT INTO service VALUES (NULL, ?, ?, ?, ?)', row)

# Read the services file
flows_file = sys.argv[3]
if not os.path.isfile(flows_file):
	print "Could not open file %s" % flows_file
	sys.exit(4)
flows = json.loads(open(flows_file, 'r').read())

# Add flows to database
for flow in flows:
	row = [str(flow['name']), str(flow['description'])]
	c.execute('INSERT INTO flow VALUES (NULL, ?, ?)', row)
	
# Add normal flow
c.execute('INSERT INTO flow VALUES (NULL, ?, ?)', ['normal', 'normal flow'])

# Build firewall
import firewall
firewall.build(c)

# Output some nice statistics
import statistics
statistics.print_all(c)

# Close database file
conn.commit()
conn.close()