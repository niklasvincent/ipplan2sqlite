#!/usr/bin/ruby
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

require 'rubygems'
require 'sqlite3'
require 'pp'

db_file = File.dirname(File.expand_path(__FILE__)) + '/../../../ipplan.db'

# Open database and print SQLite version
if File.file?(db_file)
  db = SQLite3::Database.new( db_file )
  version = db.execute('SELECT SQLITE_VERSION()')
  puts version[0]
else
  puts "No database file found: #{db_file}"
end

## EXAMPLE USAGE, PLEASE REMOVE
sql = db.execute('SELECT sql FROM sqlite_master WHERE type = "table" AND name = "network"')
puts sql[0]
db.execute('''SELECT * FROM network WHERE name LIKE "%CREW%"''').each { |network|
  pp network
}

#############################
#   INSERT YOUR CODE HERE   #
#############################

db.close