Zadanie zostało wykonane przy użyciu języka python oraz bazy danych sqlite. Wybrałam Pythona ze względu na łatwość implementacji ponieważ uznałam, że najprościej w nim będzie edytować dane (m.inn. wyodrębnieć datę itd.). SQLite zostało przeze mnie wybrane z uwagi na wsparcie Pythona dla tej bazy danych.

----------------------------------------
Schemat bazy danych:

TRACKS:
track_id (primary key),
song_id
artist
title

SAMPLES:
user_id,
song_id
date_id (foreign key references dates(id)

DATES:
id (PRIMARY KEY autoincremented),
day,
month,
year.
-----------------------------------------------
Wykonała: Katarzyna Jóźwiak, indeks nr 127234
zajęcia: poniedziałek 15:10
grupa I4