#!/usr/bin/perl
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

use strict;
use DBI;
use File::Basename;
use Cwd 'abs_path';

my $dbh;

use constant DB_FILE => dirname(abs_path($0)) . '/../../../ipplan.db';

if ( -e DB_FILE ) {
	$dbh = DBI->connect(          
	    "dbi:SQLite:dbname=" . DB_FILE, 
	    "",                          
	    "",                          
	    { RaiseError => 1 },         
	) or die $DBI::errstr;
	
	# Print SQLite version
	my $sth = $dbh->prepare("SELECT SQLITE_VERSION()");
	$sth->execute();
	my $ver = $sth->fetch();
	print @$ver . "\n";
	
} else {
	print "No database file found: %s", DB_FILE
}

## EXAMPLE USAGE, PLEASE REMOVE
my $sth = $dbh->prepare('SELECT sql FROM sqlite_master WHERE type = "table" AND name = "network"');
$sth->execute();
my $sql = $sth->fetch();
print @$sql . "\n";


#db.execute('''SELECT * FROM network WHERE name LIKE "%CREW%"''')
#print db.fetchall()

#############################
#   INSERT YOUR CODE HERE   #
#############################


$sth->finish();
$dbh->disconnect();