# run with:
#    python server.py 8000

from bottle import get, post, run, request, static_file, redirect
import os
import sys
import sqlite3
import traceback
from bottle import response
from json import dumps


MORTALITYDB = "database.sqlite"

def group_by (rows,field):
    values = set([r[field] for r in rows])
    grouped_rows = {}
    for (value,rows) in [(value,[r for r in rows if r[field]==value]) for value in values]:
        grouped_rows[value] = rows
    return grouped_rows

def pullData ():
    conn = sqlite3.connect(MORTALITYDB)
    cur = conn.cursor()

    try: 
        # cur.execute("""SELECT INSTNM, STABBR, NPT4_PROG, SATVRMID, SATMTMID, UGDS, YEAR
        cur.execute("""SELECT INSTNM, STABBR, COSTT4_A, SATVRMID, SATMTMID, SATWRMID, UGDS, YEAR, ADM_RATE
                        FROM Scorecard
                        WHERE COSTT4_A!= '' AND SATVRMID != '' AND SATMTMID != '' != ADM_RATE != ''
                        """)
        data = [{"college": college,
                "cost": cost,
                "state": state,
                "verbal": verbal,
                "math": math,
                "writing": writing,
                "students": students,
                "year": year,
                "rate": rate} for (college, state, cost, verbal, math, writing, students, year, rate) in cur.fetchall()]
                
        returnJson = []
        groupedData = group_by(data, "state")

        conn.close()

        return groupedData #could be sorted

        #return sorted(groupedData, key = lambda groupedData: groupedData["state"])

    except: 
        print "ERROR!!!"
        conn.close()
        raise

# get all data
@get("/data")
def data ():
    return pullData()

@get('/<name>')
def static (name="index.html"):
    return static_file(name, root='.')  # os.getcwd())


def main (p):
    run(host='0.0.0.0', port=p)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        print "Usage: server <port>"
