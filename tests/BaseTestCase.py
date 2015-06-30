import json
import os
import sqlite3
import sys
import yaml
from collections import namedtuple

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib'))
sys.path.insert(1, path)
import processor
import tables


def namedtuple_factory(cursor, row):
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", fields)
    return Row(*row)


class BaseTestCase(object):

    def _query(self, q):
        return self.c.execute(q).fetchall()

    def _open(self, filename, callback):
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
        with open(filename, 'r') as f:
            return callback(f)

    def _load(self, f):
        return self._open(f, lambda x: x.readlines())

    def _load_JSON(self, f):
        return self._open(f, lambda x: json.load(x))

    def _load_YAML(self, f):
        return self._open(f, lambda x: yaml.load(x.read()))

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = namedtuple_factory
        self.c = self.conn.cursor()
        tables.create(self.conn)

    def tearDown(self):
        self.conn.close()
        self.c = None
