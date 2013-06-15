<?php
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

##
# Full SQlite documentation at http://php.net/manual/en/book.sqlite3.php
##

# Use the ipplan.db file generated in the parent directory when generate.py is done
define('DB_FILE', dirname(__FILE__) . '/../../../ipplan.db');

if ( file_exists(DB_FILE) ) {
	# Open the databas file
	$db = new SQLite3(DB_FILE, SQLITE3_OPEN_READONLY);
	$result = $db->query('SELECT SQLITE_VERSION()');
	$version = $result->fetchArray(SQLITE3_NUM);
	echo $version[0] . PHP_EOL;
} else {
	printf('No database file found: %s', DB_FILE);
	exit(1);
}

## EXAMPLE USAGE, PLEASE REMOVE
$result = $db->query('SELECT sql FROM sqlite_master WHERE type = "table" AND name = "network"');
$res = $result->fetchArray(SQLITE3_ASSOC);
echo $res['sql'];
$result = $db->query('SELECT * FROM network WHERE name LIKE "%CREW%"');
while( $res = $result->fetchArray(SQLITE3_ASSOC) ) {
	print_r($res);
}

#############################
#   INSERT YOUR CODE HERE   #
#############################

$db->close();

?>