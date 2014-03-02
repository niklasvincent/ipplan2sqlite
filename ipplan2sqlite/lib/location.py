import re
from collections import namedtuple
Square = namedtuple( 'Square', ['x1', 'x2', 'y1', 'y2'] )

def add_coordinates( seatmap, cursor ):
  halls = {}
  tables = {}
  for seat in seatmap:
    hall = seat['hall'][0]
    table = seat['row']
    seat["row"] = hall + re.sub("[^0-9]", "", str(seat["row"]))
    halls.setdefault(hall, []).append(seat)
    tables.setdefault(hall, {}).setdefault(seat["row"], []).append(seat)

  switches = switches_by_table( cursor )

  for hall in halls:
    for table in tables[hall].iterkeys():
      coordinates = c = table_location( table, tables )
      row = [table, hall, c.x1, c.x2, c.y1, c.y2]
      cursor.execute( 'INSERT INTO table_coordinates VALUES(?, ?, ?, ?, ?, ?)', row )

      n = len( switches.get( table, [] ) )
      if n:
        locations = zip( switches[table], switch_locations( coordinates, n ) )
        for switch_name, location in locations:
          row = [switch_name, location[0], location[1]]
          cursor.execute( 'INSERT INTO switch_coordinates VALUES(?, ?, ?)', row) 

def switch_locations(c, n):
  locations = []
  x_len = max( c.x1, c.x2 ) - min( c.x1, c.x2 )
  x_start = min( c.x1, c.x2 )
  y_len = max( c.y1, c.y2 ) - min( c.y1, c.y2 )
  y_start = min( c.y1, c.y2 )

  horizontal = x_len > y_len

  if horizontal:
    for i in range(1, 2 * n, 2):
      x = x_start + (x_len/n)/2 * i
      y = y_start + y_len/2
      locations.append((x, y))
      locations.reverse() 
  else:
    for i in range(1, 2 * n, 2):
      x = x_start + x_len/2
      y = y_start + (y_len/n)/2 * i
      locations.append((x, y))

  return locations

def table_location(table, tables):
  seats = sorted( tables[table[0]][table], key=lambda seat: int( seat['seat'] ) )
  return Square(
      int(seats[-1]["x1"]), 
      int(seats[-1]["y1"]), 
      int(seats[0]["x1"]), 
      int(seats[0]["y1"]))

def switches_by_table(cursor):
  switches = {}
  sql ='''SELECT switch_name FROM active_switch'''
  for switch in cursor.execute( sql ).fetchall():
    table = switch[0].split('-')[0].upper()
    table = table[0] + table[1:].lstrip('0')
    switches[table] = switches.get( table, [] )
    switches[table].append( switch[0] )
  return switches
