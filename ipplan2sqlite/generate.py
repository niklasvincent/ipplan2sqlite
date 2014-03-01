#!/usr/bin/env python2

from __future__ import with_statement
import argparse
import json
import logging
import re
import os
import platform
import sys

root = logging.getLogger()
ch = logging.StreamHandler( sys.stdout )
formatter = logging.Formatter( '%(asctime)s - ipplan2sqlite - %(levelname)s - %(message)s' )
ch.setFormatter( formatter )
root.addHandler( ch )

try:
  import sqlite3
except ImportError:
  print "Could not import sqlite3. Make sure it is installed."
  sys.exit( 1 )

""" Make sure library is in our PYTHONPATH """
path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
if not path in sys.path:
    sys.path.insert( 1, path )
del path

import firewall
import networks
import parser
import statistics
import tables

SYNTAX = parser.SYNTAX

""" Parse command line arguments """
args_parser = argparse.ArgumentParser()
args_parser.add_argument( "--debug", help="Increase output verbosity", action="store_true" )
args_parser.add_argument( "--ipplan", help="Path to ipplan file", required=True)
args_parser.add_argument( "--database", help="Path to final SQLite database", required=True )
args_parser.add_argument( "--services", help="Path to services file", required=True )
args_parser.add_argument( "--flows", help="Path to flows file", required=True )
args = args_parser.parse_args()

# Adjust logging to desired verbosity
if args.debug:
  ch.setLevel( logging.DEBUG )
  root.setLevel( logging.DEBUG )
else:
  ch.setLevel( logging.INFO )
  root.setLevel( logging.INFO )

logging.debug( 'Using Python %s', platform.python_version() )

# Create fresh database file
logging.debug( 'Checking if database file %s exists', args.database )
if os.path.isfile( args.database ):
        logging.debug( 'Found existing database file %s, deleting', args.database )
        try:
          os.unlink( args.database )
	except Exception as e:
          logging.erro( 'Could not delete previous database file %s', args.database )
          sys.exit( 2 )
try:
  conn = sqlite3.connect( args.database )
  c = conn.cursor()
  c.execute('SELECT SQLITE_VERSION()')
  data = c.fetchone()
  logging.debug( "SQLite version: %s", data[0] )
except lite.Error, e:
  logging.error( 'Error when opening database %s: %s', args.database, e )
  sys.exit( 3 )

# Create tables
logging.debug( 'Creating database tables' )
tables.create( conn )

# Read the ipplan file
logging.debug( 'Checking if ipplan file %s exists', args.ipplan )
if not os.path.isfile( args.ipplan ):
  logging.error( 'No such ipplan file: %s', args.ipplan )
  sys.exit( 4 )
logging.debug( 'Found ipplan file %s', args.ipplan )

# Parse ipplan
logging.debug( 'Parsing lines in %s', args.ipplan )
lines = []
try:
  with open( args.ipplan, 'r' ) as f:
    for line in f.readlines():
      lines.append( line.strip().split() )
except Exception as e:
  logging.error( 'Could not parse ipplan file %s: %s', args.ipplan, e )

# Extract VLANs
logging.debug( 'Extracting VLANs from parsed ipplan' )
vlan = None
for l in lines:
  if len(l) == 0:
    continue
  parser_func = parser.parser_func( l )
  if parser_func:
    parse_using = getattr( parser, parser_func, vlan )
    result = parse_using( l, c, vlan )
    if not result is None:
      vlan = result

# Add custom networks
logging.debug( 'Adding custom networks' )
networks.add_all(c)

# Read the services file
logging.debug( 'Checking if services file %s exists', args.services )
if not os.path.isfile( args.services ):
        logging.error( 'No such services file: %s', args.services )
	sys.exit( 5 )
logging.debug( 'Found services file %s', args.services )
logging.debug( 'Parsing services file as JSON' )
try:
  with open( args.services, 'r' ) as f:
    services = json.loads( f.read() )
except Exception as e:
  logging.error( 'Could not parse services file %s as JSON: %s', args.services, e )
  sys.exit( 6 )

# Add services to database
logging.debug( 'Adding services to database' )
try:
  for service in services:
    row = [str(service['service']), str(service['description']), str(service['destport']), str(service['sourceport'])]
    logging.debug( 'Adding service \'%s\'', row[0] )
    c.execute('INSERT INTO service VALUES (NULL, ?, ?, ?, ?)', row)
except Exception as e:
  logging.error( 'Could not add services to database: %s', e )

# Read the flows file
logging.debug( 'Checking if flows file \'%s\' exists', args.flows )
if not os.path.isfile( args.flows ):
        logging.error( 'No such flows file: \'%s\'', args.flows )
	sys.exit( 7 )
logging.debug( 'Found flows file \'%s\'', args.flows )
logging.debug( 'Parsing flows file as JSON' )
try:
  with open( args.flows, 'r' ) as f:
    flows = json.loads( f.read() )
except Exception as e:
  logging.error( 'Could not parse flows file \'%s\' as JSON: %s', args.flows, e )

# Add flows to database
try:
  for flow in flows:
    row = [str(flow['name']), str(flow['description'])]
    logging.debug( 'Adding flow \'%s\'', row[0] )
    c.execute('INSERT INTO flow VALUES (NULL, ?, ?)', row)
except Exception as e:
  logging.error( 'Could not add services to database: %s', e )
  sys.exit( 8 )

# Add normal flow
logging.debug( 'Adding flow \'normal\'' )
c.execute('INSERT INTO flow VALUES (NULL, ?, ?)', ['normal', 'normal flow'])

# Build firewall
logging.debug( 'Building firewall rules' )
firewall.build(c)

# Output some nice statistics
statistics.print_all( c, logging )

# Close database file
logging.debug( 'Committing database' )
try:
  conn.commit()
except Exception as e:
  logging.error( 'Could not commit database \'%s\': %s', args.database, e )
  sys.exit( 9 )

logging.debug( 'Closing database' )
try:
  conn.close()
except Exception as e:
  logging.error( 'Could not close database \'%s\': %s', args.database, e )
  sys.exit( 10 )
