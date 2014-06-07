import json
import os
import sqlite3
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib'))
sys.path.insert(1, path)
import parser
import tables


class BaseTestCase(object):

    def _query(self, q):
        return self.c.execute(q).fetchall()

    def _load(self, f):
        f = os.path.abspath(os.path.join(os.path.dirname(__file__), f))
        with open(f, 'r') as f:
            lines = f.readlines()
        return lines

    def _load_JSON(self, f):
        f = os.path.abspath(os.path.join(os.path.dirname(__file__), f))
        with open(f, 'r') as f:
            data = json.load(f)
        return data

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        tables.create(self.conn)

    def tearDown(self):
        self.conn.close()
        self.c = None
