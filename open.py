# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:37:26 2020

@author: michal
"""

import sqlite3
conn=sqlite3.connect('database.db')
print("BD otwarta")
conn.execute('CREATE TABLE posty(id INTEGER PRIMARY KEY,user TEXT not null, tekst TEXT)')
conn.execute('CREATE TABLE users( name TEXT not null, password TEXT not null,imie text,nazwisko text,adres text,opis text)')
print("Tabela utworzona ")
cur=conn.cursor()
conn.close()