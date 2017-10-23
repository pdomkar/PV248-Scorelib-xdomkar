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