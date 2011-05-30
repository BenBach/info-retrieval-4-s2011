#!/usr/bin/python

import freebase
import string
import codecs

sports_query = [{
      "id":    None,
      "name":  None,
      "type":  "/sports/sport"
    }]

sports = freebase.mqlreaditer(sports_query, asof=None)

f = codecs.open('gazetteer_lists/sports2.lst', 'w', encoding="utf-8")

for sport in sports:
    words = string.split(sport.name)

    f.write(string.join([string.lower(w) for w in words]))
    f.write("\n")
    f.write(string.join([string.upper(w) for w in words]))
    f.write("\n")
    f.write(string.join([string.capitalize(w) for w in words]))
    f.write("\n")

f.close()
