#!/usr/bin/python
#
# Copyright (c) 2013, Niklas Lindblad <niklas@lindblad.info>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import sqlite3, os, sys

# Use the ipplan.db file generated in the parent directory when generate.py is done
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../ipplan.db'))

if os.path.isfile(DB_FILE):
    try:
        conn = sqlite3.connect(DB_FILE)
        db = conn.cursor()

        db.execute('SELECT SQLITE_VERSION()')
        data = db.fetchone()
        print "SQLite version: %s" % data

    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
        sys.exit(1)

else:
    print "No database file found: %s" % DB_FILE
    sys.exit(2)

## EXAMPLE USAGE, PLEASE REMOVE
db.execute('''SELECT sql FROM sqlite_master WHERE type = "table" AND name = "network"''')
print str(db.fetchone()[0])
db.execute('''SELECT * FROM network WHERE name LIKE "%CREW%"''')
print db.fetchall()

#############################
#   INSERT YOUR CODE HERE   #
#############################

db.close()
