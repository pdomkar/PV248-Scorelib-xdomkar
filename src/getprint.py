import sys
import sqlite3
import json

def main():
    conn = sqlite3.connect( "../data/scorelib.dat" )
    if len(sys.argv) == 2:
        printId = sys.argv[1]
    else:
        print("not retrieve input")
        return

    cur = conn.cursor()
    cur.execute( "select person.name from person join score_author on person.id = score_author.composer join score on score_author.score = score.id join edition on score.id = edition.score join print on edition.id = print.edition where print.id = {}".format(printId))
    result = cur.fetchall()

    d = []
    for row in result:
        d.append({"composer": row[0]})

    print(json.dumps(d))

    with open('../data/data.json', 'w') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
