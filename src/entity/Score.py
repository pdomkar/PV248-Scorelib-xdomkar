from entity.DBItem import DBItem

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
