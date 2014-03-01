import os
import sqlite3
import sys
import unittest
from BaseTestCase import BaseTestCase

path = os.path.abspath( os.path.join( os.path.dirname( __file__ ), '../lib' ) )
sys.path.insert( 1, path )
import firewall
import networks
import parser
import tables

class TestFirewall(BaseTestCase, unittest.TestCase):

  def setUp(self):
    super( TestFirewall, self ).setUp()
    firewall.add_services( self._load_JSON( 'data/services.json' ), self.c )
    firewall.add_flows( self._load_JSON( 'data/flows.json' ), self.c )
    networks.add_all( self.c )
    parser.parse( self._load( 'data/masterNetwork.txt' ), self.c )

  def testServerClientRules(self):
    lines = self._load( 'data/testServerClientRules.txt' )
    parser.parse( lines, self.c )
    firewall.build( self.c )
    rules = self._query( 'SELECT * FROM firewall_rule_ip_level' )
    self.assertEquals( len( rules ), 1, "Wrong number of firewall rules" )
  
    rule = self._query( 'SELECT from_node_name, to_node_name, flow_name, service_dst_ports FROM firewall_rule_ip_level' )[0]
    self.assertEquals( rule[0], 'jumpgate1.event.dreamhack.se', "Wrong source host" )
    self.assertEquals( rule[1], 'ddns1.event.dreamhack.se', "Wrong destination host" )
    self.assertEquals( rule[2], 'normal', "Wrong flow" )
    self.assertEquals( rule[3], '2022/tcp', "Wrong destination port/protocol" )


def main():
  unittest.main()

if __name__ == '__main__':
  main()
