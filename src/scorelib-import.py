from collections import Counter
import re
import sqlite3
from entity.Person import Person
from entity.Score import Score
# -mrun

# class represent statistic of loaded data and print statistic abut composer a centuries
class ProcessStatistic:
    def __init__(self):
        self.countAuthors = Counter()
        self.countCenturies = Counter()

    def processData(self, person):
        self.countAuthors[person.name] += 1
        if person.born is not None:
            self.countCenturies[int(str(person.born)[:2])] += 1

    def printStatistic(self):
        print('Composers:')
        for key, value in self.countAuthors.items():
            print('{}: {}'.format(key, value))
        print('Centuries:')
        for key, value in sorted(self.countCenturies.items()):
            print('{}th century: {}'.format(key, value))


class ProcessScoreLib:
    def __init__(self):
        self.lastTitle = None
        self.composers = []

    # Process a single line of input.
    def process(self,  key, value, conn, processStatistic ):
        if key == 'Composer':
            self.storeOldScoreAuthor(conn)
            self.composers = []
            for c in value.split(';'):
                p = Person( conn, c.strip() )
                processStatistic.processData(p)
                pId = p.store()
                self.composers.append(pId)
        if key == 'Title':
            s = Score( conn, value)
            s.store()
            self.lastTitle = s.name
        if key in ['Genre', 'Key', 'Composition Year', 'Incipit']:
            if not self.lastTitle is None:
                res = Score.fetch_item(conn, self.lastTitle)
                if not res is None:
                    score = Score(conn, res[1])
                    score.id = res[0]
                    score.genre = (value if key == 'Genre' else res[2])
                    score.key = (value if key == 'Key' else res[3])
                    score.incipit = (value if key == 'Incipit' else res[4])
                    score.year = (value if key == 'Composition Year' else res[5])
                    score.store()

    def storeOldScoreAuthor(self, conn):
        cursor = conn.cursor()
        scoreId = None
        cursor.execute("SELECT id FROM score WHERE name = ?", (self.lastTitle,))
        res = cursor.fetchone()
        if not res is None:
            scoreId = res[0]
        if not scoreId is None:
            for i in self.composers:
                cursor.execute("INSERT INTO score_author (score, composer) VALUES (?, ?)", (scoreId, i))
            conn.commit()



# main - Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
def main():
    conn = sqlite3.connect( '../data/scorelib-my.dat' )
    processStatistic = ProcessStatistic()
    processScoreLib = ProcessScoreLib()
    rx = re.compile( r"(.*): (.*)" )
    for line in open( '../data/scorelib.txt', 'r', encoding='utf-8' ):
        m = rx.match( line )
        if m is None:
            continue
        processScoreLib.process( m.group( 1 ), m.group( 2 ), conn, processStatistic )

    # processStatistic.printStatistic()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
