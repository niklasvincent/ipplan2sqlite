import os
import sqlite3
import sys
import unittest

path = os.path.abspath( os.path.join( os.path.dirname( __file__ ), '../lib' ) )
sys.path.insert( 1, path )
import parser

class TestParser(unittest.TestCase):

  def setUp(self):
    self.conn = sqlite3.connect(':memory:')

  def testParseIPv4(self):
    self.assertEquals( parser.ip2long( '8.8.8.8', 4 ), 134744072 )
    self.assertEquals( parser.ip2long( '77.80.251.247/32', 4 ), 1297153015 )

  def testParserMapping(self):
    self.assertEquals( parser.parser_func( ["#$ d20--b.event.dreamhack.local\t\t\t10.0.3.45\t\t\tipv4f;ipv4r;tblswmgmt"] ), "host" )
    self.assertEquals( parser.parser_func( ["""TECH-SRV-1-INT 						D-FW-V		77.80.231.0/27		921	othernet"""]) , "network" )
    self.assertEquals( parser.parser_func( ["""#@ IPV4-NET      77.80.128.0/17"""] ), "master_network" )

def main():
  unittest.main()

if __name__ == '__main__':
  main()
