#!/bin/bash

sqlite3 ../../ipplan.db "SELECT name || ':cisco:up' FROM host WHERE name LIKE '%-sw.event.dreamhack.local' OR name LIKE '%-st.event.dreamhack.local';"