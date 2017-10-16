from collections import Counter
import re
import sqlite3

# -mrun


# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).
class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.conn = conn
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if self.id is None :
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]
            return self.id
        else:
            self.do_update()
            return self.id


# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.
class Person(DBItem):
    def __init__( self,  conn, string ):
        super().__init__( conn )
        self.born = self.died = None
        self.name = re.sub( '\([0-9/+-]+\)', '', string ).strip()
        m = re.search( "([0-9]+)--([0-9]+)", string )
        if not m is None:
            self.born = int( m.group( 1 ) )
            self.died = int( m.group( 2 ) )

    def fetch_id(self):
        self.cursor.execute("SELECT id FROM person WHERE name = ?", (self.name,))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]


    def do_store(self):
        self.cursor.execute("INSERT INTO person (name, born, died) VALUES (?, ?, ?)", (self.name, self.born, self.died))
        self.conn.commit()

    def do_update(self):
        self.cursor.execute("UPDATE person SET name=?, born=?, died=? WHERE id=?", (self.name, self.born, self.died, self.id))
        self.conn.commit()

    def to_string(self):
        print('Person: {}, born: {}, die: {}'.format(self.name, self.born, self.died))

#Class represent Score table
class Score(DBItem):
    def __init__( self,  conn, title ):
        super().__init__( conn )
        self.genre = self.key = self.incipit = self.year = None
        self.name = title.strip()

    def fetch_id(self):
        self.cursor.execute("SELECT id FROM score WHERE name = ?", (self.name,))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    @staticmethod  # use as decorator
    def fetch_item(conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, genre, key, incipit, year FROM score WHERE name = ?", (name,))
        res = cursor.fetchone()
        return res

    def do_store(self):
        self.cursor.execute("INSERT INTO score (name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)", (self.name, self.genre, self.key, self.incipit, self.year))
        self.conn.commit()

    def do_update(self):
        self.cursor.execute("UPDATE score SET name=?, genre=?, key=?, incipit=?, year=? WHERE id=?", (self.name, self.genre, self.key, self.incipit, self.year, self.id))
        self.conn.commit()

    def to_string(self):
        print('Score: {}, name: {}, genre: {}, key: {}, incipit: {}, year: {}'.format(self.id, self.name, self.genre, self.key, self.incipit, self.year))



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
