from entity.DBItem import DBItem
import re
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
