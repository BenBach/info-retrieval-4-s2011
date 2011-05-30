#!/usr/bin/python

#
# you need to have the freebase python library installed (http://code.google.com/p/freebase-python)
#

import freebase
import string
import codecs

def write_perms(word, f, split=True):
    if split:
        words = string.split(word)
    else:
        words = [word]

    f.write(string.join([string.lower(w) for w in words]))
    f.write("\n")
    f.write(string.join([string.upper(w) for w in words]))
    f.write("\n")
    f.write(string.join([string.capitalize(w) for w in words]))
    f.write("\n")

    return None

f_defs = codecs.open('gazetteer_lists/definitions.def', 'w', encoding="utf-8")

####################################################################################################
# sports
####################################################################################################

sports_query = [{
      "id":    None,
      "name":  None,
      "type":  "/sports/sport"
    }]

sports = freebase.mqlreaditer(sports_query, asof=None)

f_sports = codecs.open('gazetteer_lists/sports.lst', 'w', encoding="utf-8")

for sport in sports:
    write_perms(sport.name, f_sports)

f_sports.close()

f_defs.write("sports.lst:sport\n")

####################################################################################################
# teams
####################################################################################################

teams_query = [{
      "id":            None,
      "name":          None,
      "abbreviation":  None,
      "type":          "/sports/sports_team"
    }]

teams = freebase.mqlreaditer(teams_query, asof=None)

f_teams = codecs.open('gazetteer_lists/teams.lst', 'w', encoding='utf-8')
f_team_abbrevs = codecs.open('gazetteer_lists/team_abbrevs.lst', 'w', encoding='utf-8')

for team in teams:
    write_perms(team.name, f_teams)

    if team.abbreviation != None:
        write_perms(team.abbreviation, f_team_abbrevs, split=False)

f_teams.close()
f_team_abbrevs.close()

f_defs.write("teams.lst:team\n")
f_defs.write("team_abbrevs.lst:team:team_abbrev\n")

####################################################################################################
# athletes
####################################################################################################

athletes_query = [{
      "/common/topic/alias": [{
        "index":    None,
        "lang":     "/lang/en",
        "optional": True,
        "type":     "/type/text",
        "value":    None
      }],
      "id":    None,
      "name":  None,
      "type":  "/sports/pro_athlete"
    }]

athletes = freebase.mqlreaditer(athletes_query, asof=None)

f_athlete_aliases = codecs.open('gazetteer_lists/athlete_aliases.lst', 'w', encoding='utf-8')

athlete_names = set()

for athlete in athletes:
    athlete_sub_names = set(string.split(athlete.name))
    athlete_names |= athlete_sub_names

    if athlete["/common/topic/alias"] != None:
        for alias in athlete["/common/topic/alias"]:
            write_perms(alias.value, f_athlete_aliases, split=False)

f_athlete_aliases.close()

f_athletes = codecs.open('gazetteer_lists/athletes.lst', 'w', encoding='utf-8')

for athlete in athlete_names:
    write_perms(athlete, f_athletes, split=False)

f_athletes.close()

f_defs.write("athletes.lst:athlete\n")
f_defs.write("athlete_aliases.lst:athlete:athlete_alias\n")

f_defs.close()
