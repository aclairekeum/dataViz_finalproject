# run with:
#    python mortality-server-2.py 8080

from bottle import get, post, run, request, static_file, redirect
import os
import sys
import sqlite3
import traceback
from bottle import response
from json import dumps


MORTALITYDB = "database.sqlite"

def pullData ():
    conn = sqlite3.connect(MORTALITYDB)
    cur = conn.cursor()

    try: 
        cur.execute("""SELECT INSTNM, STABBR, SATVRMID, SATMTMID, SATWRMID FROM Scorecard WHERE STABBR = 'HI'""")
        data = [{"college": college,
                "state": state,} for (college, state, verbal, math, writing) in cur.fetchall()]
        conn.close()
        # data = [{"year":int(year),
        #          "count":int(countid)
        #         } for (year, countid,) in  cur.fetchall()]
        # conn.close()

        college = list(set([r["college"] for r in data]))
        print college
        #return {"year":year, "data":data}

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
