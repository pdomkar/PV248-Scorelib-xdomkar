import sys
import sqlite3
import json

def getScores(cur, cName):
    cur.execute( "select id, name FROM person where person.name LIKE \"%{}%\"".format(cName))
    result = cur.fetchall()

    d = []
    for row in result:
        cur.execute("SELECT score.name FROM score JOIN score_author ON score_author.score = score.id WHERE score_author.composer = {}".format(row[0]))
        result2 = cur.fetchall()
        scores = []
        for sc in result2:
            scores.append({"name": sc[0]})
        d.append({"composer": row[1], "scores": scores})

    return d

def main():
    conn = sqlite3.connect( "../data/scorelib.dat" )
    if len(sys.argv) == 2:
        cName = sys.argv[1]
    else:
        print("not retrieve composer name")
        return

    cur = conn.cursor()
    result = getScores(cur, cName)


    print(json.dumps(result))
    with open('../data/data_search.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
