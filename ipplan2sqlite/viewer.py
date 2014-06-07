import argparse
import logging
import os
import sys
from Tkinter import *
import ttk

""" Make sure library is in our PYTHONPATH """
path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
if not path in sys.path:
    sys.path.insert(1, path)

from layout import Rectangle
from layout import Dot

try:
    import sqlite3
except ImportError:
    print "Could not import sqlite3. Make sure it is installed."
    sys.exit(1)


def add_table(canvas, table, scale=1):
    if scale != 1:
        table = Rectangle(*[scale * i for i in list(table)])
    canvas.create_rectangle(
        table.x1,
        table.y1,
        table.x2,
        table.y2,
        fill="green")


def add_switch(canvas, switch, scale=1):
    size = 2 * scale
    canvas.create_rectangle(
        switch.x - size,
        switch.y - size,
        switch.x + size,
        switch.y + size,
        fill="red")


def setup_logging():
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - dh-layout - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    ch.setLevel(logging.DEBUG)
    root.setLevel(logging.DEBUG)


def parse_arguments():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--database",
        help="Path to ipplan SQLite database file",
        required=True)
    args_parser.add_argument("--hall", help="Hall to draw", required=True)
    args = args_parser.parse_args()
    return args


def setup_db(filename):
    try:
        conn = sqlite3.connect(filename)
        return conn
    except Exception as e:
        logging.error('Could not open SQLite database \'%s\'', filename)
        sys.exit(1)


def get_tables(db, hall):
    sql = """SELECT x1, x2, y1, y2, x_start, y_start, width, height, horizontal
             FROM table_coordinates WHERE hall = '%s'"""
    sql = sql % hall
    return [Rectangle(*t) for t in db.cursor().execute(sql).fetchall()]


def get_switches(db, hall):
    sql = """SELECT x, y
          FROM switch_coordinates WHERE switch_name LIKE '{}%'""".format(
        hall)
    return [Dot(*s) for s in db.cursor().execute(sql).fetchall()]


def main():

    setup_logging()
    args = parse_arguments()

    db = setup_db(args.database)

    master = Tk()

    master.title("Dreamhack Layout")
    master.configure(background='black')
    width, height = master.winfo_screenwidth(), master.winfo_screenheight()
    w = Canvas(master, width=width, height=height, background='black')
    w.pack()

    for t in get_tables(db, args.hall):
        add_table(w, t, scale=2)

    for s in get_switches(db, args.hall):
        add_switch(w, s, scale=2)

    mainloop()

if __name__ == '__main__':
    main()
