import re
from collections import namedtuple
Square = namedtuple( 'Square', ['x1', 'x2', 'y1', 'y2', 'x_start', 'y_start', 
    'width', 'height', 'horizontal'] )
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
      row = [table, hall, c.x1, c.x2, c.y1, c.y2, c.x_start, c.y_start, 
              c.width, c.height, c.horizontal]
      cursor.execute( 'INSERT INTO table_coordinates VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row )

      n = len( switches.get( table, [] ) )
      if n:
        locations = zip( switches[table], switch_locations( coordinates, n ) )
        for switch_name, location in locations:
          row = [switch_name, location[0], location[1]]
          cursor.execute( 'INSERT INTO switch_coordinates VALUES(?, ?, ?)', row) 

def switch_locations(t, n):
  locations = []

  if t.horizontal:
    for i in range(1, 2 * n, 2):
      x = t.x_start + (t.width/n)/2 * i
      y = t.y_start + t.height/2
      locations.append((x, y))
      locations.reverse() 
  else:
    for i in range(1, 2 * n, 2):
      x = t.x_start + t.height/2
      y = t.y_start + (t.width/n)/2 * i
      locations.append((x, y))

  return locations

def table_location(table, tables):
  seats = sorted( tables[table[0]][table], key=lambda seat: int( seat['seat'] ) )
  x1 = int( seats[-1]["x1"] )
  x2 = int( seats[0]["x2"] )
  y1 = int( seats[-1]["y1"] )
  y2 = int( seats[0]["y2"] )
  x_len = max( x1, x2 ) - min( x1, x2 )
  y_len = max( y1, y2 ) - min( y1, y2 )
  x_start = min( x1, x2 )
  y_start = min( y1, y2 )
  horizontal = 1 if x_len > y_len else 0
  width = x_len if horizontal else y_len
  height = y_len if horizontal else x_len

  return Square( x1, y1, x2, y2, x_start, y_start, width, height, horizontal )

def switches_by_table(cursor):
  switches = {}
  sql ='''SELECT switch_name FROM active_switch'''
  for switch in cursor.execute( sql ).fetchall():
    table = switch[0].split('-')[0].upper()
    table = table[0] + table[1:].lstrip('0')
    switches[table] = switches.get( table, [] )
    switches[table].append( switch[0] )
  return switches
